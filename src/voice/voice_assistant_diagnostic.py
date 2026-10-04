import os
import sys
import time
import threading
import traceback

import sounddevice as sd
import numpy as np
from openwakeword.model import Model
from faster_whisper import WhisperModel

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.core.brain import Brain
from src.core.router import CommandRouter
from src.voice.tts import MyXTTS


SAMPLE_RATE = 16000
DEVICE = 1
BLOCK_SIZE = 1280

WAKE_THRESHOLD = 0.35
WAKE_COOLDOWN = 2.0

WAIT_SECONDS = 10


class MyXVoiceDiagnostic:

    def __init__(self):

        print("==========================================")
        print("      MYX VOICE DIAGNOSTIC TEST")
        print("==========================================")

        self.running = False
        self.processing = False
        self.last_detection_time = 0.0

        print("[System] Starting Router...")
        self.router = CommandRouter()

        print("[System] Starting Brain...")
        self.brain = Brain(self_router=self.router)

        print("[TTS] Starting...")
        self.tts = MyXTTS()
        print("[TTS] Ready")

        print("[Wake] Loading HEY JARVIS...")
        self.wake_model = Model(
            wakeword_models=["hey_jarvis"],
            inference_framework="onnx"
        )
        print("[Wake] Ready")

        print()
        print("==========================================")
        print("DIAGNOSTIC FLOW")
        print("==========================================")
        print("HEY JARVIS")
        print("    ↓")
        print("Wake detected")
        print("    ↓")
        print("TTS response")
        print("    ↓")
        print("10 SECOND WAIT")
        print("    ↓")
        print("Diagnostic result")
        print("==========================================")
        print()

    def audio_callback(self, indata, frames, time_info, status):

        if status:
            print(f"[Mic] {status}")

        if not self.running:
            return

        if self.processing:
            return

        audio = indata[:, 0]

        audio = np.clip(audio, -1.0, 1.0)

        audio = (audio * 32767).astype(np.int16)

        try:

            prediction = self.wake_model.predict(audio)

            score = float(
                prediction.get("hey_jarvis", 0.0)
            )

        except Exception as e:

            print(f"[Wake ERROR] {e}")
            return

        if score >= 0.05:
            print(f"[Wake] score={score:.3f}")

        current_time = time.monotonic()

        if (
            score >= WAKE_THRESHOLD
            and current_time - self.last_detection_time
            >= WAKE_COOLDOWN
        ):

            self.last_detection_time = current_time

            print()
            print("==========================================")
            print("🔥 HEY JARVIS DETECTED!")
            print(f"Wake Score: {score:.3f}")
            print("==========================================")

            self.processing = True

            thread = threading.Thread(
                target=self.diagnostic_mode,
                daemon=True
            )

            thread.start()

    def diagnostic_mode(self):

        try:

            print()
            print("==========================================")
            print("        DIAGNOSTIC COMMAND MODE")
            print("==========================================")

            # STEP 1 — TTS
            print()
            print("[TEST 1] Starting TTS...")

            self.tts.speak(
                "Yes, how can I help?"
            )

            print("[TEST 1] TTS completed.")

            # STEP 2 — WAIT
            print()
            print("==========================================")
            print("[TEST 2] 10 SECOND WAIT")
            print("==========================================")
            print("⚠️ DO NOT PRESS CTRL+C")
            print("⚠️ DO NOT SPEAK")
            print("⚠️ JUST WAIT")
            print()

            for remaining in range(WAIT_SECONDS, 0, -1):

                print(
                    f"[WAIT] {remaining} seconds remaining..."
                )

                time.sleep(1)

            print()
            print("==========================================")
            print("✅ WAIT COMPLETED SUCCESSFULLY")
            print("==========================================")

            print()
            print("[RESULT]")
            print("TTS + 10 second wait completed.")
            print("Microphone recording was NOT started.")
            print()

        except KeyboardInterrupt:

            print()
            print("==========================================")
            print("❌ KEYBOARD INTERRUPT DETECTED")
            print("==========================================")
            print(
                "KeyboardInterrupt occurred during diagnostic_mode."
            )
            print()

        except Exception:

            print()
            print("==========================================")
            print("❌ DIAGNOSTIC ERROR")
            print("==========================================")

            traceback.print_exc()

        finally:

            self.processing = False

            print()
            print("[Diagnostic] Returning to wake listening...")
            print()

    def start(self):

        if self.running:
            print("[Voice] Already running.")
            return

        self.running = True

        print("==========================================")
        print("      MYX DIAGNOSTIC LISTENER ACTIVE")
        print("==========================================")
        print("🎤 Say: HEY JARVIS")
        print("⚠️ DO NOT PRESS CTRL+C")
        print("==========================================")
        print()

        try:

            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                device=DEVICE,
                blocksize=BLOCK_SIZE,
                callback=self.audio_callback
            ):

                while self.running:

                    time.sleep(0.1)

        except KeyboardInterrupt:

            print()
            print("==========================================")
            print("❌ CTRL+C RECEIVED IN MAIN LISTENER")
            print("==========================================")

        except Exception:

            print()
            print("==========================================")
            print("❌ VOICE SYSTEM ERROR")
            print("==========================================")

            traceback.print_exc()

        finally:

            self.running = False

            try:
                self.tts.stop()
            except Exception:
                pass

            print()
            print("[Voice] Diagnostic stopped.")

    def stop(self):

        self.running = False

        try:
            self.tts.stop()
        except Exception:
            pass


if __name__ == "__main__":

    try:

        assistant = MyXVoiceDiagnostic()

        assistant.start()

    except Exception:

        print()
        print("==========================================")
        print("       MYX DIAGNOSTIC STARTUP ERROR")
        print("==========================================")

        traceback.print_exc()
        
