import os
import sys
import time
import traceback

import sounddevice as sd
import numpy as np
from openwakeword.model import Model


# ==========================================
# PROJECT PATH SETUP
# ==========================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.voice.tts import MyXTTS


# ==========================================
# CONFIGURATION
# ==========================================

SAMPLE_RATE = 16000
DEVICE = 1
BLOCK_SIZE = 1280

TEST_SECONDS = 20

WAKE_THRESHOLD = 0.35
TTS_COOLDOWN = 5.0


# ==========================================
# START
# ==========================================

print("==========================================")
print("        MYX WAKE + TTS TEST")
print("==========================================")
print()

print("[Config]")
print(f"Microphone Device : {DEVICE}")
print(f"Sample Rate       : {SAMPLE_RATE}")
print(f"Block Size        : {BLOCK_SIZE}")
print(f"Test Duration     : {TEST_SECONDS}s")
print(f"Wake Threshold    : {WAKE_THRESHOLD}")
print(f"TTS Cooldown      : {TTS_COOLDOWN}s")
print()

print("==========================================")


# ==========================================
# TTS INITIALIZATION
# ==========================================

print("[TTS] Initializing...")

try:

    tts = MyXTTS()

    print("[TTS] Engine Ready")

except Exception:

    print()
    print("==========================================")
    print("          TTS INITIALIZATION ERROR")
    print("==========================================")

    traceback.print_exc()

    sys.exit(1)


# ==========================================
# WAKE WORD INITIALIZATION
# ==========================================

print()
print("[Wake] Loading HEY JARVIS model...")

try:

    wake_model = Model(
        wakeword_models=["hey_jarvis"],
        inference_framework="onnx"
    )

    print("[Wake] Model Ready")

except Exception:

    print()
    print("==========================================")
    print("       WAKE MODEL INITIALIZATION ERROR")
    print("==========================================")

    traceback.print_exc()

    try:
        tts.stop()
    except Exception:
        pass

    sys.exit(1)


# ==========================================
# VARIABLES
# ==========================================

callback_count = 0
detection_count = 0
best_score = 0.0

last_tts_time = 0.0


# ==========================================
# AUDIO CALLBACK
# ==========================================

def audio_callback(indata, frames, time_info, status):

    global callback_count
    global detection_count
    global best_score
    global last_tts_time

    callback_count += 1

    # --------------------------------------
    # Microphone status
    # --------------------------------------

    if status:

        print()
        print(f"[Mic Status] {status}")


    # --------------------------------------
    # Get microphone audio
    # --------------------------------------

    audio = indata[:, 0]


    # --------------------------------------
    # Convert float32 -> int16
    # --------------------------------------

    audio = np.clip(
        audio,
        -1.0,
        1.0
    )

    audio = (
        audio * 32767
    ).astype(np.int16)


    # --------------------------------------
    # Wake word prediction
    # --------------------------------------

    try:

        prediction = wake_model.predict(audio)

        score = float(
            prediction.get(
                "hey_jarvis",
                0.0
            )
        )

    except Exception as e:

        print()
        print("[Wake Prediction ERROR]")
        print(e)

        return


    # --------------------------------------
    # Best score
    # --------------------------------------

    if score > best_score:

        best_score = score


    # --------------------------------------
    # Diagnostic output
    # --------------------------------------

    if callback_count % 50 == 0:

        print(
            f"[Mic] callbacks={callback_count} "
            f"| wake_score={score:.3f} "
            f"| best={best_score:.3f}"
        )


    # --------------------------------------
    # Wake word detection
    # --------------------------------------

    current_time = time.monotonic()


    if (
        score >= WAKE_THRESHOLD
        and
        current_time - last_tts_time >= TTS_COOLDOWN
    ):

        last_tts_time = current_time

        detection_count += 1


        print()
        print("==========================================")
        print("🔥 HEY JARVIS DETECTED!")
        print(f"Wake Score : {score:.3f}")
        print(f"Detection  : #{detection_count}")
        print("==========================================")
        print()


        # ----------------------------------
        # TTS TEST
        # ----------------------------------

        print("[TTS] Speaking response...")

        try:

            tts.speak(
                "Yes, how can I help?"
            )

            print("[TTS] Response finished.")

        except Exception as e:

            print()
            print("==========================================")
            print("             TTS ERROR")
            print("==========================================")
            print(e)
            print("==========================================")


        print()
        print("[Wake] Returning to listener...")
        print()


# ==========================================
# OPEN MICROPHONE
# ==========================================

print()
print("[Mic] Opening InputStream...")

start_time = time.monotonic()


try:

    with sd.InputStream(

        samplerate=SAMPLE_RATE,

        channels=1,

        dtype="float32",

        device=DEVICE,

        blocksize=BLOCK_SIZE,

        callback=audio_callback

    ):

        print("[Mic] InputStream OPEN")
        print()

        print("==========================================")
        print("       🎤 WAKE + TTS LISTENER ACTIVE")
        print("==========================================")

        print()
        print("Say:")
        print("HEY JARVIS")

        print()
        print("This test contains:")
        print("✅ Microphone")
        print("✅ OpenWakeWord")
        print("✅ TTS")

        print()
        print("This test DOES NOT contain:")
        print("❌ Whisper")
        print("❌ Brain")
        print("❌ Command Router")
        print("❌ Command Recording")
        print("❌ Threads")

        print()
        print("⚠️ DO NOT PRESS CTRL+C")
        print(f"Test will automatically finish after {TEST_SECONDS} seconds.")

        print()
        print("==========================================")
        print()


        # ----------------------------------
        # Main test loop
        # ----------------------------------

        while (
            time.monotonic() - start_time
            < TEST_SECONDS
        ):

            elapsed = int(
                time.monotonic() - start_time
            )

            remaining = (
                TEST_SECONDS - elapsed
            )


            if elapsed > 0:

                last_second = getattr(
                    audio_callback,
                    "_last_second",
                    -1
                )

                if elapsed != last_second:

                    audio_callback._last_second = elapsed

                    print(
                        f"[Timer] {remaining:02d}s remaining..."
                    )


            time.sleep(0.1)


except KeyboardInterrupt:

    print()
    print("==========================================")
    print("❌ CTRL+C RECEIVED")
    print("==========================================")

    print()
    print("IMPORTANT:")
    print("KeyboardInterrupt occurred during Wake + TTS test.")


except Exception:

    print()
    print("==========================================")
    print("❌ WAKE + TTS TEST ERROR")
    print("==========================================")

    traceback.print_exc()


finally:

    # --------------------------------------
    # Stop TTS
    # --------------------------------------

    try:

        tts.stop()

    except Exception:

        pass


    # ======================================
    # RESULTS
    # ======================================

    print()
    print()
    print("==========================================")
    print("        WAKE + TTS TEST RESULTS")
    print("==========================================")

    print(
        f"Total callbacks : {callback_count}"
    )

    print(
        f"Detections      : {detection_count}"
    )

    print(
        f"Best wake score : {best_score:.3f}"
    )

    print("==========================================")


    if detection_count > 0:

        print()
        print("✅ WAKE WORD DETECTION WORKED")

        print()
        print("TTS was also triggered.")

        print()
        print("Next step depends on whether")
        print("CTRL+C occurred after TTS.")


    else:

        print()
        print("ℹ️ No HEY JARVIS detection occurred.")


    print()
    print("[System] Wake + TTS diagnostic finished.")
    
