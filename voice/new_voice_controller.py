import os
import time
import numpy as np
import sounddevice as sd

from openwakeword.model import Model
from faster_whisper import WhisperModel


class CHITTNewVoiceController:

    def __init__(self, score_threshold=0.4):

        self.sample_rate = 16000
        self.command_seconds = 5
        self.score_threshold = score_threshold
        self.is_running = False

        print("[CHITT New Voice] Loading Wake Engine...")

        self.wake_model = Model(
            wakeword_models=["hey_jarvis"],
            inference_framework="onnx"
        )

        print("[CHITT New Voice] Loading Faster-Whisper...")

        self.whisper = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8"
        )

        print("[CHITT New Voice] Engine Ready.")

    def listen_command(self):

        print("[CHITT] Listening for command...")

        audio = sd.rec(
            int(self.sample_rate * self.command_seconds),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            device=1
        )

        sd.wait()

        audio = audio[:, 0]

        print("[CHITT] Recognizing...")

        segments, info = self.whisper.transcribe(
            audio,
            beam_size=5
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        print(f"[CHITT] You: {text}")

        return text

    def start_listening(self, command_callback):

        self.is_running = True

        print()
        print("[CHITT New Voice] =============================")
        print("[CHITT New Voice] READY")
        print("[CHITT New Voice] Say: HEY JARVIS")
        print("[CHITT New Voice] =============================")

        def callback(indata, frames, time_info, status):

            if not self.is_running:
                return

            audio = (indata[:, 0] * 32767).astype(np.int16)

            scores = self.wake_model.predict(audio)

            score = scores.get("hey_jarvis", 0.0)

            if score >= self.score_threshold:

                print(
                    f"\n[CHITT] WAKE WORD DETECTED! "
                    f"score={score:.3f}"
                )

                command = self.listen_command()

                if command and command_callback:
                    command_callback(command)

                print("\n[CHITT] Say HEY JARVIS again...")

        try:

            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                blocksize=1280,
                device=1,
                callback=callback
            ):

                while self.is_running:
                    time.sleep(0.5)

        except KeyboardInterrupt:

            print("\n[CHITT] Stopped.")

        except Exception as e:

            print(f"\n[CHITT Voice Error]: {e}")

    def stop(self):

        self.is_running = False
