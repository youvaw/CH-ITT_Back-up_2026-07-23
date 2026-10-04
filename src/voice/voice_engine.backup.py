# -*- coding: utf-8 -*-

import ctypes
import queue
import sys
import threading
import time

import numpy as np
import sounddevice as sd
from openwakeword.model import Model

from src.voice.speech_to_text import SpeechToText
from src.voice.tts import MyXTTS


class MyXVoiceEngine:

    # ========================================================
    # AUDIO CONFIGURATION
    # ========================================================

    INPUT_DEVICE = 9

    # Realtek WASAPI microphone works at 48 kHz.
    INPUT_RATE = 48000

    # OpenWakeWord expects 16 kHz audio.
    WAKE_RATE = 16000

    # 3840 samples @ 48 kHz = 80 ms
    INPUT_BLOCK = 3840

    # 1280 samples @ 16 kHz = 80 ms
    WAKE_BLOCK = 1280

    WAKE_THRESHOLD = 0.35
    COOLDOWN_SECONDS = 2.0

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        brain=None,
        on_status=None,
        on_text=None,
        on_response=None
    ):

        print("[Voice] Initializing MyX Voice Engine...")

        self.brain = brain

        self.on_status = on_status
        self.on_text = on_text
        self.on_response = on_response

        self.running = False
        self._stop_requested = threading.Event()
        self.command_listening = False

        self.last_detection_time = 0.0

        self.stt = None
        self.tts = None

        self.audio_queue = queue.Queue(maxsize=20)

        self.wake_thread = None

        # ====================================================
        # WAKE WORD MODEL
        # ====================================================

        self.model = Model(
            wakeword_models=["hey_jarvis"],
            inference_framework="onnx"
        )

        print("[Voice] Wake Word Model Ready")
        print(f"[Voice] Device       : {self.INPUT_DEVICE}")
        print(f"[Voice] Input Rate   : {self.INPUT_RATE} Hz")
        print(f"[Voice] Wake Rate    : {self.WAKE_RATE} Hz")
        print(f"[Voice] Input Block  : {self.INPUT_BLOCK}")
        print(f"[Voice] Wake Block   : {self.WAKE_BLOCK}")
        print(f"[Voice] Threshold    : {self.WAKE_THRESHOLD}")

    # ========================================================
    # UI CALLBACKS
    # ========================================================

    def _status(self, message):

        print(f"[Voice] {message}")

        if self.on_status:

            try:
                self.on_status(message)

            except Exception:
                pass

    def _text(self, text):

        if self.on_text:

            try:
                self.on_text(text)

            except Exception:
                pass

    def _response(self, text):

        if self.on_response:

            try:
                self.on_response(text)

            except Exception:
                pass

    # ========================================================
    # AUDIO CALLBACK
    # ========================================================

    def _audio_callback(
        self,
        indata,
        frames,
        time_info,
        status
    ):

        if status:
            print(f"[Mic] {status}")

        if not self.running:
            return

        try:

            # ------------------------------------------------
            # InputStream uses dtype="float32".
            #
            # Therefore indata is already a NumPy float32
            # array. It is NOT raw int16 bytes.
            #
            # Device 9 can provide multiple channels.
            # We use channel 0 for wake-word processing.
            # ------------------------------------------------

            audio = np.asarray(
                indata,
                dtype=np.float32
            )

            if audio.size == 0:
                return

            # ------------------------------------------------
            # Stereo / multi-channel -> mono
            # ------------------------------------------------

            if audio.ndim == 2:

                # Select channel 0 deterministically; the Realtek
                # microphone array is opened as stereo, while the
                # wake-word pipeline consumes one mono signal.
                if audio.shape[1] < 1:
                    return

                audio = audio[:, 0]

            elif audio.ndim == 1:

                # Keep compatibility with a mono callback buffer.
                audio = audio.reshape(-1)

            else:

                # Reject unexpected callback dimensions instead of
                # flattening interleaved channels into a bad sequence.
                return

            if audio.shape[0] != frames:
                return

            # ------------------------------------------------
            # Make an independent contiguous copy.
            # ------------------------------------------------

            audio = np.asarray(
                audio,
                dtype=np.float32
            ).copy()

            if audio.size == 0:
                return

            # Safety normalization.
            audio = np.clip(
                audio,
                -1.0,
                1.0
            )

            # ------------------------------------------------
            # Queue audio for wake worker.
            # ------------------------------------------------

            try:

                self.audio_queue.put_nowait(audio)

            except queue.Full:

                # Remove oldest block so the microphone
                # processing does not become delayed.

                try:

                    self.audio_queue.get_nowait()

                except queue.Empty:

                    pass

                try:

                    self.audio_queue.put_nowait(audio)

                except queue.Full:

                    pass

        except Exception as e:

            print(f"[Mic ERROR] {e}")

    # ========================================================
    # AUDIO PROCESSING
    # ========================================================

    def _process_audio(self, audio):

        audio = np.asarray(
            audio,
            dtype=np.float32
        )

        if audio.size == 0:
            return None

        audio = np.clip(
            audio,
            -1.0,
            1.0
        )

        return audio

    # ========================================================
    # 48 kHz -> 16 kHz RESAMPLER
    # ========================================================
    #
    # 48000 / 16000 = 3
    #
    # Therefore every 3 input samples become 1 output
    # sample.
    #
    # We use a simple 3-sample averaging filter before
    # decimation. This removes part of the high-frequency
    # content and gives OpenWakeWord a clean 16 kHz stream.
    #
    # IMPORTANT:
    # No SciPy is required here.
    #
    # ========================================================

    def _resample_48k_to_16k(self, audio):

        audio = np.asarray(
            audio,
            dtype=np.float32
        )

        if audio.size < 3:
            return np.empty(
                0,
                dtype=np.float32
            )

        usable_length = (
            audio.size // 3
        ) * 3

        if usable_length == 0:
            return np.empty(
                0,
                dtype=np.float32
            )

        audio = audio[:usable_length]

        # ------------------------------------------------
        # 3-sample averaging low-pass filter + decimation.
        #
        # 48 kHz:
        #
        # [s0 s1 s2] [s3 s4 s5] [s6 s7 s8] ...
        #
        # becomes:
        #
        # [(s0+s1+s2)/3]
        # [(s3+s4+s5)/3]
        # [(s6+s7+s8)/3]
        # ------------------------------------------------

        reshaped = audio.reshape(-1, 3)

        resampled = (
            reshaped[:, 0]
            + reshaped[:, 1]
            + reshaped[:, 2]
        ) / 3.0

        return np.asarray(
            resampled,
            dtype=np.float32
        )

    # ========================================================
    # WAKE WORD WORKER
    # ========================================================

    def _wake_worker(self):

        print(
            "[Voice] Wake inference worker started."
        )

        # ------------------------------------------------
        # Continuous 48 kHz microphone buffer
        # ------------------------------------------------

        input_buffer = np.empty(
            0,
            dtype=np.float32
        )

        # ------------------------------------------------
        # Continuous 16 kHz wake-word buffer
        # ------------------------------------------------

        wake_buffer = np.empty(
            0,
            dtype=np.int16
        )

        blocks = 0

        while self.running:

            try:

                audio = self.audio_queue.get(
                    timeout=0.2
                )

            except queue.Empty:

                continue

            try:

                audio = self._process_audio(
                    audio
                )

                if audio is None:
                    continue

                # ------------------------------------------------
                # Add microphone data to 48 kHz buffer.
                # ------------------------------------------------

                input_buffer = np.concatenate(
                    (
                        input_buffer,
                        audio
                    )
                )

                # ------------------------------------------------
                # Process complete 3840-sample blocks.
                #
                # 3840 @ 48 kHz
                # =
                # 1280 @ 16 kHz
                # ------------------------------------------------

                while (
                    len(input_buffer)
                    >= self.INPUT_BLOCK
                ):

                    input_block = input_buffer[
                        :self.INPUT_BLOCK
                    ]

                    input_buffer = input_buffer[
                        self.INPUT_BLOCK:
                    ]

                    # ------------------------------------------------
                    # CHITT internal resampling.
                    #
                    # SciPy is NOT used.
                    # ------------------------------------------------

                    wake_audio = (
                        self._resample_48k_to_16k(
                            input_block
                        )
                    )

                    if wake_audio.size == 0:
                        continue

                    wake_audio = np.clip(
                        wake_audio,
                        -1.0,
                        1.0
                    )

                    # ------------------------------------------------
                    # OpenWakeWord accepts PCM int16.
                    # ------------------------------------------------

                    wake_audio = (
                        wake_audio * 32767.0
                    ).astype(
                        np.int16
                    )

                    # ------------------------------------------------
                    # Add to wake buffer.
                    # ------------------------------------------------

                    wake_buffer = np.concatenate(
                        (
                            wake_buffer,
                            wake_audio
                        )
                    )

                    # ------------------------------------------------
                    # Feed exact 1280-sample blocks to
                    # OpenWakeWord.
                    # ------------------------------------------------

                    while (
                        len(wake_buffer)
                        >= self.WAKE_BLOCK
                    ):

                        block = wake_buffer[
                            :self.WAKE_BLOCK
                        ]

                        wake_buffer = wake_buffer[
                            self.WAKE_BLOCK:
                        ]

                        prediction = self.model.predict(
                            block
                        )

                        score = float(
                            prediction.get(
                                "hey_jarvis",
                                0.0
                            )
                        )

                        blocks += 1

                        # ------------------------------------------------
                        # Debug score.
                        # ------------------------------------------------

                        if score >= 0.05:

                            print(
                                f"[Wake] score={score:.3f}"
                            )

                        # ------------------------------------------------
                        # Wake detection.
                        # ------------------------------------------------

                        now = time.monotonic()

                        if (
                            score >= self.WAKE_THRESHOLD
                            and
                            (
                                now
                                -
                                self.last_detection_time
                            )
                            >= self.COOLDOWN_SECONDS
                            and
                            not self.command_listening
                        ):

                            self.last_detection_time = now

                            print()

                            print(
                                "=================================================="
                            )

                            print(
                                "          ★ HEY JARVIS DETECTED ★"
                            )

                            print(
                                f"Wake Score : {score:.3f}"
                            )

                            print(
                                "=================================================="
                            )

                            self._status(
                                "HEY JARVIS detected"
                            )

                            self._start_command_listener()

            except Exception as e:

                print(
                    f"[Wake Worker ERROR] {e}"
                )

        print(
            "[Voice] Wake inference worker stopped."
        )

    # ========================================================
    # COMMAND LISTENER START
    # ========================================================

    def _start_command_listener(self):

        if self.command_listening:
            return

        self.command_listening = True

        threading.Thread(
            target=self._listen_for_command,
            daemon=True
        ).start()

    # ========================================================
    # COMMAND LISTENER
    # ========================================================

    def _listen_for_command(self):

        try:

            self._status(
                "Listening for command..."
            )

            print()

            print(
                "--------------------------------------------------"
            )

            print(
                "MYX COMMAND LISTENER"
            )

            print(
                "Speak your command..."
            )

            print(
                "--------------------------------------------------"
            )

            # ------------------------------------------------
            # Speech-to-Text
            # ------------------------------------------------

            self.stt = SpeechToText(
                model_size="base",
                sample_rate=48000,
                device=self.INPUT_DEVICE,
                record_seconds=5
            )

            command = self.stt.listen()

            command = str(
                command or ""
            ).strip()

            if not command:

                self._status(
                    "No command recognized."
                )

                return

            print(
                f"[Voice] Command: {command}"
            )

            self._text(
                command
            )

            # ------------------------------------------------
            # BRAIN
            # ------------------------------------------------

            if self.brain is None:

                response = (
                    "MyX Brain is not connected."
                )

            else:

                try:

                    response = self.brain.process(
                        command
                    )

                except Exception as e:

                    print(
                        f"[Brain ERROR] {e}"
                    )

                    response = (
                        "I couldn't process that command."
                    )

            if response is None:

                response = ""

            response = str(
                response
            ).strip()

            # ------------------------------------------------
            # UI RESPONSE
            # ------------------------------------------------

            if response:

                self._response(
                    response
                )

                print(
                    f"[Voice] Response: {response}"
                )

                # ------------------------------------------------
                # TEXT TO SPEECH
                # ------------------------------------------------

                try:

                    if self.tts is None:

                        self.tts = MyXTTS()

                    self.tts.speak(
                        response
                    )

                except Exception as e:

                    print(
                        f"[TTS ERROR] {e}"
                    )

        except Exception as e:

            print(
                f"[Command ERROR] {e}"
            )

            self._status(
                f"Command error: {e}"
            )

        finally:

            self.command_listening = False

            self.stt = None

            self._status(
                "Wake listener ready."
            )

    # ========================================================
    # WINDOWS AUDIO THREAD INITIALIZATION
    # ========================================================

    def _initialize_audio_com(self):

        if sys.platform != "win32":
            return False

        ole32 = ctypes.WinDLL(
            "ole32",
            use_last_error=True
        )
        ole32.CoInitializeEx.argtypes = [
            ctypes.c_void_p,
            ctypes.c_ulong
        ]
        ole32.CoInitializeEx.restype = ctypes.c_long
        ole32.CoUninitialize.argtypes = []
        ole32.CoUninitialize.restype = None

        # WASAPI may be opened from MyX's background worker. COM must
        # be initialized on that same thread before PortAudio starts it.
        hr = ole32.CoInitializeEx(
            None,
            0  # COINIT_MULTITHREADED
        )
        unsigned_hr = hr & 0xFFFFFFFF

        if hr in (0, 1):  # S_OK or S_FALSE; both require CoUninitialize.
            return True

        if unsigned_hr == 0x80010106:  # RPC_E_CHANGED_MODE; already initialized.
            return False

        raise OSError(
            f"Windows audio COM initialization failed (HRESULT 0x{unsigned_hr:08X})."
        )

    @staticmethod
    def _uninitialize_audio_com():

        ole32 = ctypes.WinDLL(
            "ole32",
            use_last_error=True
        )
        ole32.CoUninitialize()

    # ========================================================
    # START
    # ========================================================

    def start(self):

        if self._stop_requested.is_set():
            return

        if self.running:

            print(
                "[Voice] Voice system already running."
            )

            return

        self.running = True

        # A stop can arrive between the initial check and this assignment.
        if self._stop_requested.is_set():
            self.running = False
            return

        print()

        print(
            "============================================================"
        )

        print(
            "              MYX VOICE SYSTEM ACTIVE"
        )

        print(
            "============================================================"
        )

        print(
            "Wake Word : HEY JARVIS"
        )

        print(
            "STT       : Whisper"
        )

        print(
            "Brain     : Connected"
            if self.brain is not None
            else
            "Brain     : Not Connected"
        )

        print(
            "TTS       : pyttsx3"
        )

        print(
            "Resampler : CHITT Internal 48kHz -> 16kHz"
        )

        print(
            "============================================================"
        )

        # ----------------------------------------------------
        # Wake worker
        # ----------------------------------------------------

        self.wake_thread = threading.Thread(
            target=self._wake_worker,
            daemon=True
        )

        self.wake_thread.start()

        # ----------------------------------------------------
        # Microphone
        # ----------------------------------------------------

        com_initialized = False

        try:

            com_initialized = self._initialize_audio_com()

            with sd.InputStream(
                samplerate=self.INPUT_RATE,
                channels=2,
                dtype="float32",
                device=self.INPUT_DEVICE,
                blocksize=self.INPUT_BLOCK,
                callback=self._audio_callback
            ):

                print(
                    "[Mic] WASAPI InputStream OPEN"
                )

                print(
                    "[Voice] Say: HEY JARVIS"
                )

                while self.running:

                    time.sleep(
                        0.1
                    )

        except Exception as e:

            print()

            print(
                "=================================================="
            )

            print(
                "[Voice ERROR]"
            )

            print(
                e
            )

            print(
                "=================================================="
            )

            self._status(
                f"Voice system error: {e}"
            )

        finally:

            self.running = False

            if com_initialized:

                try:
                    self._uninitialize_audio_com()
                except Exception:
                    self._status(
                        "Windows audio thread cleanup warning."
                    )

            print(
                "[Voice] Voice system stopped."
            )

    # ========================================================
    # STOP
    # ========================================================

    def stop(self):

        # Also record a stop issued before start() begins.
        self._stop_requested.set()

        if not self.running:
            return

        print(
            "[Voice] Stopping voice system..."
        )

        self.running = False

        # ------------------------------------------------
        # Wait briefly for wake worker.
        # ------------------------------------------------

        if hasattr(
            self,
            "wake_thread"
        ):

            if (
                self.wake_thread is not None
                and
                self.wake_thread.is_alive()
            ):

                self.wake_thread.join(
                    timeout=1.0
                )

        # ------------------------------------------------
        # Stop TTS if initialized.
        # ------------------------------------------------

        if self.tts is not None:

            try:

                self.tts.stop()

            except Exception:

                pass

        self.tts = None
        self.stt = None
        self.command_listening = False

        print(
            "[Voice] Voice system stopped"
        )


# ============================================================
# DIRECT MODULE TEST
# ============================================================

if __name__ == "__main__":

    engine = MyXVoiceEngine()

    try:

        engine.start()

    except KeyboardInterrupt:

        print()

        print(
            "[Voice] Keyboard interrupt received."
        )

    finally:

        engine.stop()
        