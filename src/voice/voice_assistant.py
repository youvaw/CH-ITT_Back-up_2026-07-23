import os
import sys
import time
import wave
import traceback
import queue

import sounddevice as sd
import numpy as np

from openwakeword.model import Model
from faster_whisper import WhisperModel


# ============================================================
# PROJECT PATH
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# MYX CORE
# ============================================================

from src.core.brain import Brain
from src.core.router import CommandRouter
from src.voice.tts import MyXTTS


# ============================================================
# SETTINGS
# ============================================================

SAMPLE_RATE = 16000
DEVICE = 1
BLOCK_SIZE = 1280

# HEY JARVIS detection
WAKE_THRESHOLD = 0.20
WAKE_COOLDOWN = 2.0

# After command finishes
POST_COMMAND_COOLDOWN = 5.0

# Smart command listening
SPEECH_START_TIMEOUT = 5.0
SILENCE_DURATION = 0.7
MAX_COMMAND_SECONDS = 8.0
SPEECH_THRESHOLD = 0.03

# Small delay after TTS
COMMAND_START_DELAY = 0.35

# Keep latest command audio for debugging
DEBUG_WAV_FILE = os.path.join(
    PROJECT_ROOT,
    "myx_last_command.wav"
)


# ============================================================
# MYX VOICE ASSISTANT
# ============================================================

class MyXVoiceAssistant:

    def __init__(self):

        print("==========================================")
        print("       MYX VOICE ASSISTANT")
        print("==========================================")

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        self.running = False
        self.wake_event = False
        self.last_detection_time = 0.0

        # ----------------------------------------------------
        # Router
        # ----------------------------------------------------

        print("[3/4] Starting Command Router...")

        self.router = CommandRouter()

        # ----------------------------------------------------
        # Brain
        # ----------------------------------------------------

        print("[System] Starting Brain...")

        self.brain = Brain(
            self_router=self.router
        )

        print("[Brain] Ready")

        # ----------------------------------------------------
        # Wake Word
        # ----------------------------------------------------

        print("[1/4] Loading HEY JARVIS model...")

        self.wake_model = Model(
            wakeword_models=["hey_jarvis"],
            inference_framework="onnx"
        )

        print("[Wake] Model Ready")

        # ----------------------------------------------------
        # Whisper
        # ----------------------------------------------------

        print("[2/4] Loading Whisper BASE model...")

        self.whisper_model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

        print("[Whisper] Model Ready")

        # ----------------------------------------------------
        # TTS
        # ----------------------------------------------------

        print("[4/4] Starting TTS...")

        self.tts = MyXTTS()

        print("[TTS] Ready")

        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------

        print()
        print("==========================================")
        print("       MYX VOICE SYSTEM READY")
        print("==========================================")

        print()
        print("[Voice] Configuration")
        print("------------------------------------------")
        print(f"Microphone Device : {DEVICE}")
        print(f"Sample Rate       : {SAMPLE_RATE}")
        print(f"Block Size        : {BLOCK_SIZE}")
        print(f"Wake Threshold    : {WAKE_THRESHOLD}")
        print(f"Wake Cooldown     : {WAKE_COOLDOWN}s")
        print(f"Speech Timeout    : {SPEECH_START_TIMEOUT}s")
        print(f"Silence Duration  : {SILENCE_DURATION}s")
        print(f"Max Command Time  : {MAX_COMMAND_SECONDS}s")
        print(f"Speech Threshold  : {SPEECH_THRESHOLD}")
        print(f"Debug WAV         : {DEBUG_WAV_FILE}")
        print("------------------------------------------")


    # ========================================================
    # AUDIO LEVEL
    # ========================================================

    def get_audio_level(self, audio):

        if audio is None or len(audio) == 0:
            return 0.0

        audio = np.asarray(
            audio,
            dtype=np.float32
        )

        rms = np.sqrt(
            np.mean(
                np.square(audio)
            )
        )

        return float(rms)


    # ========================================================
    # AUDIO PEAK
    # ========================================================

    def get_audio_peak(self, audio):

        if audio is None or len(audio) == 0:
            return 0.0

        audio = np.asarray(
            audio,
            dtype=np.float32
        )

        return float(
            np.max(
                np.abs(audio)
            )
        )


    # ========================================================
    # WAKE WORD CALLBACK
    # ========================================================

    def audio_callback(
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

        # ----------------------------------------------------
        # If wake already detected, ignore callbacks
        # ----------------------------------------------------

        if self.wake_event:
            return

        # ----------------------------------------------------
        # Microphone audio
        # ----------------------------------------------------

        try:

            audio = indata[:, 0]

            audio = np.clip(
                audio,
                -1.0,
                1.0
            )

            audio_int16 = (
                audio * 32767
            ).astype(np.int16)

        except Exception as e:

            print(f"[Mic ERROR] {e}")
            return

        # ----------------------------------------------------
        # Wake prediction
        # ----------------------------------------------------

        try:

            prediction = self.wake_model.predict(
                audio_int16
            )

            score = float(
                prediction.get(
                    "hey_jarvis",
                    0.0
                )
            )

        except Exception as e:

            print(f"[Wake ERROR] {e}")
            return

        # ----------------------------------------------------
        # Debug score
        # ----------------------------------------------------

        if score >= 0.05:

            print(
                f"[Wake] score={score:.3f}"
            )

        # ----------------------------------------------------
        # Wake detection
        # ----------------------------------------------------

        current_time = time.monotonic()

        if (
            score >= WAKE_THRESHOLD
            and
            current_time - self.last_detection_time
            >= WAKE_COOLDOWN
        ):

            self.last_detection_time = current_time

            print()
            print("==========================================")
            print("🔥 HEY JARVIS DETECTED!")
            print(f"Wake Score: {score:.3f}")
            print("==========================================")

            # Only notify main loop.
            # Do NOT open another microphone stream here.

            self.wake_event = True


    # ========================================================
    # SMART COMMAND RECORDING
    # ========================================================

    def record_smart_command(self):

        print()
        print("==========================================")
        print("      🎤 SMART COMMAND LISTENING")
        print("==========================================")
        print("Speak your command...")
        print()

        audio_queue = queue.Queue()

        recording_started = False
        speech_start_time = None
        last_speech_time = None

        collected_audio = []

        # ----------------------------------------------------
        # Command microphone callback
        # ----------------------------------------------------

        def command_callback(
            indata,
            frames,
            time_info,
            status
        ):

            if status:
                print(
                    f"[Command Mic] {status}"
                )

            try:

                audio = indata[:, 0].copy()

                audio_queue.put(
                    audio
                )

            except Exception as e:

                print(
                    f"[Command Mic ERROR] {e}"
                )


        # ----------------------------------------------------
        # Open command microphone
        # ----------------------------------------------------

        try:

            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                device=DEVICE,
                blocksize=BLOCK_SIZE,
                callback=command_callback
            ):

                start_time = time.monotonic()

                while True:

                    current_time = time.monotonic()

                    # ------------------------------------------------
                    # Speech start timeout
                    # ------------------------------------------------

                    if (
                        not recording_started
                        and
                        current_time - start_time
                        >= SPEECH_START_TIMEOUT
                    ):

                        print()
                        print(
                            "[Command] No speech detected."
                        )

                        return None


                    # ------------------------------------------------
                    # Get microphone block
                    # ------------------------------------------------

                    try:

                        audio = audio_queue.get(
                            timeout=0.2
                        )

                    except queue.Empty:

                        continue


                    # ------------------------------------------------
                    # Calculate speech level
                    # ------------------------------------------------

                    level = self.get_audio_level(
                        audio
                    )

                    current_time = time.monotonic()


                    # ------------------------------------------------
                    # Waiting for speech
                    # ------------------------------------------------

                    if not recording_started:

                        if level >= SPEECH_THRESHOLD:

                            recording_started = True

                            speech_start_time = (
                                current_time
                            )

                            last_speech_time = (
                                current_time
                            )

                            collected_audio.append(
                                audio
                            )

                            print(
                                f"[Command] Speech detected "
                                f"(level={level:.4f})"
                            )

                        continue


                    # ------------------------------------------------
                    # Already recording speech
                    # ------------------------------------------------

                    collected_audio.append(
                        audio
                    )

                    if level >= SPEECH_THRESHOLD:

                        last_speech_time = (
                            current_time
                        )

                    # ------------------------------------------------
                    # Maximum command time
                    # ------------------------------------------------

                    if (
                        current_time - speech_start_time
                        >= MAX_COMMAND_SECONDS
                    ):

                        print(
                            "[Command] Maximum command "
                            "time reached."
                        )

                        break

                    # ------------------------------------------------
                    # Silence detection
                    # ------------------------------------------------

                    if (
                        last_speech_time is not None
                        and
                        current_time - last_speech_time
                        >= SILENCE_DURATION
                    ):

                        print(
                            "[Command] Speech ended."
                        )

                        break


        except Exception:

            print()
            print("==========================================")
            print("     COMMAND MICROPHONE ERROR")
            print("==========================================")

            traceback.print_exc()

            return None


        # ----------------------------------------------------
        # No audio
        # ----------------------------------------------------

        if not collected_audio:

            print(
                "[Command] No audio captured."
            )

            return None


        # ----------------------------------------------------
        # Combine audio blocks
        # ----------------------------------------------------

        try:

            audio_data = np.concatenate(
                collected_audio
            )

            audio_data = np.clip(
                audio_data,
                -1.0,
                1.0
            )

            audio_int16 = (
                audio_data * 32767
            ).astype(np.int16)

        except Exception as e:

            print(
                f"[Command] Audio processing error: {e}"
            )

            return None


        duration = (
            len(audio_int16) /
            SAMPLE_RATE
        )

        rms = self.get_audio_level(
            audio_data
        )

        peak = self.get_audio_peak(
            audio_data
        )

        print(
            f"[Command] Captured {duration:.2f}s"
        )

        print(
            f"[Command] RMS: {rms:.4f}"
        )

        print(
            f"[Command] Peak: {peak:.4f}"
        )

        return audio_int16


    # ========================================================
    # SAVE WAV
    # ========================================================

    def save_wav(self, audio):

        try:

            with wave.open(
                DEBUG_WAV_FILE,
                "wb"
            ) as wf:

                wf.setnchannels(1)

                wf.setsampwidth(2)

                wf.setframerate(
                    SAMPLE_RATE
                )

                wf.writeframes(
                    audio.tobytes()
                )

            print()
            print(
                f"[Audio] Debug WAV saved:"
            )

            print(
                DEBUG_WAV_FILE
            )

            return DEBUG_WAV_FILE

        except Exception as e:

            print(
                f"[Audio] WAV save error: {e}"
            )

            traceback.print_exc()

            return None


    # ========================================================
    # COMMAND MODE
    # ========================================================

    def command_mode(self):

        filename = None

        try:

            print()
            print("==========================================")
            print("        MYX COMMAND MODE")
            print("==========================================")

            # ------------------------------------------------
            # TTS prompt
            # ------------------------------------------------

            self.tts.speak(
                "Yes, how can I help?"
            )

            time.sleep(
                COMMAND_START_DELAY
            )

            # ------------------------------------------------
            # Smart microphone recording
            # ------------------------------------------------

            audio = self.record_smart_command()

            if audio is None:

                self.tts.speak(
                    "I didn't hear a command."
                )

                return


            # ------------------------------------------------
            # Save WAV
            # ------------------------------------------------

            filename = self.save_wav(
                audio
            )

            if filename is None:

                self.tts.speak(
                    "I could not process the audio."
                )

                return


            # ------------------------------------------------
            # Whisper
            # ------------------------------------------------

            print()
            print("==========================================")
            print("       WHISPER TRANSCRIPTION")
            print("==========================================")

            print(
                "[Whisper] Transcribing..."
            )

            segments, info = (
                self.whisper_model.transcribe(
                    filename,
                    language="en",
                    beam_size=5,
                    vad_filter=False,
                    condition_on_previous_text=False
                )
            )


            # ------------------------------------------------
            # Whisper information
            # ------------------------------------------------

            detected_language = getattr(
                info,
                "language",
                None
            )

            language_probability = getattr(
                info,
                "language_probability",
                None
            )

            print(
                f"[Whisper] Detected language: "
                f"{detected_language}"
            )

            if language_probability is not None:

                print(
                    f"[Whisper] Language probability: "
                    f"{language_probability:.2f}"
                )


            # ------------------------------------------------
            # Collect transcription
            # ------------------------------------------------

            text_parts = []

            for segment in segments:

                segment_text = (
                    segment.text.strip()
                )

                if segment_text:

                    print(
                        f"[Whisper Segment] "
                        f"{segment_text}"
                    )

                    text_parts.append(
                        segment_text
                    )


            text = " ".join(
                text_parts
            ).strip()


            # ------------------------------------------------
            # Show transcription
            # ------------------------------------------------

            print()
            print("==========================================")
            print("YOU SAID:")
            print(
                text
                if text
                else "(nothing detected)"
            )
            print("==========================================")


            # ------------------------------------------------
            # Empty command
            # ------------------------------------------------

            if not text:

                print(
                    "[Brain] No command detected."
                )

                self.tts.speak(
                    "I didn't understand the command."
                )

                return


            # ------------------------------------------------
            # Brain
            # ------------------------------------------------

            print()
            print(
                "[Brain] Processing command..."
            )

            try:

                response = self.brain.process(
                    text
                )

            except Exception as e:

                response = (
                    f"Brain error: {e}"
                )

                print(
                    f"[Brain ERROR] {e}"
                )


            # ------------------------------------------------
            # Response
            # ------------------------------------------------

            print()
            print("==========================================")
            print("MYX RESPONSE:")
            print(response)
            print("==========================================")


            # ------------------------------------------------
            # TTS response
            # ------------------------------------------------

            self.tts.speak(
                response
            )


        except Exception:

            print()
            print("==========================================")
            print("       MYX COMMAND ERROR")
            print("==========================================")

            traceback.print_exc()


        finally:

            # ------------------------------------------------
            # IMPORTANT:
            # Do NOT delete the WAV.
            #
            # It is intentionally kept for debugging.
            # ------------------------------------------------

            pass


    # ========================================================
    # WAKE LISTENING
    # ========================================================

    def listen_for_wake_word(self):

        self.wake_event = False

        print()
        print("==========================================")
        print("      🎤 MYX IS LISTENING")
        print("==========================================")

        print(
            "Listening for: HEY JARVIS"
        )

        print(
            f"Wake Threshold: {WAKE_THRESHOLD}"
        )

        print("==========================================")

        try:

            # ------------------------------------------------
            # Wake stream only.
            # It closes before command recording.
            # ------------------------------------------------

            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                device=DEVICE,
                blocksize=BLOCK_SIZE,
                callback=self.audio_callback
            ):

                while (
                    self.running
                    and
                    not self.wake_event
                ):

                    time.sleep(
                        0.05
                    )


        except Exception as e:

            print()
            print("==========================================")
            print("       WAKE MICROPHONE ERROR")
            print("==========================================")

            print(e)

            traceback.print_exc()

            return False


        return self.wake_event


    # ========================================================
    # MAIN START LOOP
    # ========================================================

    def start(self):

        if self.running:

            print(
                "[Voice] Already running."
            )

            return


        self.running = True

        print()
        print("==========================================")
        print("      🎤 MYX VOICE SYSTEM ACTIVE")
        print("==========================================")

        print(
            "Listening for: HEY JARVIS"
        )

        print(
            f"Wake Threshold: {WAKE_THRESHOLD}"
        )

        print(
            f"Microphone Device: {DEVICE}"
        )

        print(
            f"Sample Rate: {SAMPLE_RATE}"
        )

        print(
            "Press CTRL+C to stop."
        )

        print("==========================================")


        try:

            while self.running:

                # ------------------------------------------------
                # STEP 1
                # Wake word listening
                # ------------------------------------------------

                detected = (
                    self.listen_for_wake_word()
                )


                if not self.running:

                    break


                if not detected:

                    time.sleep(
                        0.2
                    )

                    continue


                # ------------------------------------------------
                # STEP 2
                # Command mode
                #
                # Wake microphone is already closed.
                # ------------------------------------------------

                self.command_mode()


                if not self.running:

                    break


                # ------------------------------------------------
                # STEP 3
                # Post-command cooldown
                # ------------------------------------------------

                print()
                print(
                    f"[Voice] Post-command cooldown: "
                    f"{POST_COMMAND_COOLDOWN}s"
                )

                time.sleep(
                    POST_COMMAND_COOLDOWN
                )


                # ------------------------------------------------
                # STEP 4
                # Return to wake listening
                # ------------------------------------------------

                print()
                print(
                    "[Voice] Returning to "
                    "wake-word listening..."
                )

                print()


        except KeyboardInterrupt:

            print()
            print(
                "[Voice] Keyboard interrupt."
            )


        except Exception as e:

            print()
            print("==========================================")
            print("          MYX VOICE ERROR")
            print("==========================================")

            print(e)

            traceback.print_exc()


        finally:

            self.running = False

            print()
            print("==========================================")
            print("       MYX VOICE SYSTEM STOPPED")
            print("==========================================")


    # ========================================================
    # STOP
    # ========================================================

    def stop(self):

        self.running = False


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        assistant = MyXVoiceAssistant()

        assistant.start()

    except KeyboardInterrupt:

        print()
        print(
            "[MYX] Stopped by user."
        )

    except Exception:

        print()
        print("==========================================")
        print("       MYX STARTUP ERROR")
        print("==========================================")

        traceback.print_exc()
        
