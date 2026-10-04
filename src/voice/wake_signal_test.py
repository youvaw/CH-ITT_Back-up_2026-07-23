import time
import sounddevice as sd
import numpy as np
from openwakeword.model import Model


SAMPLE_RATE = 16000
DEVICE = 1
BLOCK_SIZE = 1280
TEST_SECONDS = 20
WAKE_THRESHOLD = 0.35


print("==========================================")
print("       MYX WAKE SIGNAL DIAGNOSTIC")
print("==========================================")
print()

print("[Config]")
print(f"Device       : {DEVICE}")
print(f"Sample Rate  : {SAMPLE_RATE}")
print(f"Block Size   : {BLOCK_SIZE}")
print(f"Duration     : {TEST_SECONDS}s")
print(f"Threshold    : {WAKE_THRESHOLD}")
print()

print("[Wake] Loading HEY JARVIS model...")

wake_model = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx"
)

print("[Wake] Model Ready")
print()

callback_count = 0
best_score = 0.0
best_rms = 0.0
best_max = 0.0
best_mean_abs = 0.0


def audio_callback(indata, frames, time_info, status):
    global callback_count
    global best_score
    global best_rms
    global best_max
    global best_mean_abs

    callback_count += 1

    if status:
        print(f"[Mic Status] {status}")

    audio = indata[:, 0]

    rms = float(np.sqrt(np.mean(audio ** 2)))
    max_value = float(np.max(np.abs(audio)))
    mean_abs = float(np.mean(np.abs(audio)))

    if rms > best_rms:
        best_rms = rms

    if max_value > best_max:
        best_max = max_value

    if mean_abs > best_mean_abs:
        best_mean_abs = mean_abs

    audio_int16 = np.clip(
        audio,
        -1.0,
        1.0
    )

    audio_int16 = (
        audio_int16 * 32767
    ).astype(np.int16)

    try:
        prediction = wake_model.predict(audio_int16)

        score = float(
            prediction.get("hey_jarvis", 0.0)
        )

    except Exception as e:
        print()
        print("[Wake ERROR]")
        print(e)
        return

    if score > best_score:
        best_score = score

    if callback_count % 25 == 0:

        print(
            f"[Diagnostic] "
            f"callbacks={callback_count} "
            f"| RMS={rms:.6f} "
            f"| MAX={max_value:.6f} "
            f"| MEAN={mean_abs:.6f} "
            f"| WAKE={score:.3f} "
            f"| BEST={best_score:.3f}"
        )


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
        print("       🎤 SIGNAL TEST ACTIVE")
        print("==========================================")
        print()
        print("First speak normally for a few seconds.")
        print()
        print("Then say:")
        print("HEY JARVIS")
        print()
        print("Say it clearly 2-3 times.")
        print()
        print("DO NOT PRESS CTRL+C")
        print(f"Test ends automatically after {TEST_SECONDS}s.")
        print("==========================================")
        print()

        last_second = -1

        while time.monotonic() - start_time < TEST_SECONDS:

            elapsed = int(
                time.monotonic() - start_time
            )

            if elapsed != last_second:

                last_second = elapsed

                remaining = TEST_SECONDS - elapsed

                print(
                    f"[Timer] {remaining:02d}s remaining..."
                )

            time.sleep(0.1)

except KeyboardInterrupt:

    print()
    print("❌ CTRL+C RECEIVED")

except Exception as e:

    print()
    print("==========================================")
    print("❌ SIGNAL TEST ERROR")
    print("==========================================")
    print(e)


print()
print()
print("==========================================")
print("       WAKE SIGNAL TEST RESULTS")
print("==========================================")
print()

print(f"Total callbacks : {callback_count}")
print(f"Best RMS        : {best_rms:.6f}")
print(f"Best MAX        : {best_max:.6f}")
print(f"Best Mean Abs   : {best_mean_abs:.6f}")
print(f"Best Wake Score : {best_score:.3f}")

print()
print("==========================================")

if best_score >= WAKE_THRESHOLD:

    print("✅ HEY JARVIS DETECTED")

elif best_score > 0.10:

    print("⚠️ Wake signal detected, but below threshold")

else:

    print("❌ Very low wake score")

print()
print("[System] Wake signal diagnostic finished.")

