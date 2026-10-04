import time
import traceback

import sounddevice as sd


SAMPLE_RATE = 16000
DEVICE = 1
BLOCK_SIZE = 1280
TEST_SECONDS = 15


print("==========================================")
print("        MYX MICROPHONE LISTENER TEST")
print("==========================================")
print()
print(f"Device      : {DEVICE}")
print(f"Sample Rate : {SAMPLE_RATE}")
print(f"Block Size  : {BLOCK_SIZE}")
print(f"Duration    : {TEST_SECONDS} seconds")
print()
print("⚠️ DO NOT PRESS CTRL+C")
print("⚠️ Just wait for the test to finish.")
print()
print("==========================================")
print()


running = True
callback_count = 0


def audio_callback(indata, frames, time_info, status):

    global callback_count

    callback_count += 1

    if status:
        print(f"[Mic Status] {status}")

    if callback_count % 50 == 0:
        print(
            f"[Mic] InputStream active | callbacks={callback_count}"
        )


try:

    print("[Mic] Opening InputStream...")

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
        print("🎤 MICROPHONE LISTENER ACTIVE")
        print()

        start_time = time.monotonic()

        while time.monotonic() - start_time < TEST_SECONDS:

            elapsed = int(
                time.monotonic() - start_time
            )

            remaining = TEST_SECONDS - elapsed

            print(
                f"[Timer] {remaining:02d}s remaining...",
                end="\r",
                flush=True
            )

            time.sleep(1)

        print()
        print()

    print("==========================================")
    print("✅ TEST COMPLETED")
    print("==========================================")
    print()
    print(f"Total callbacks: {callback_count}")
    print()
    print("No KeyboardInterrupt occurred.")
    print("Microphone InputStream is working normally.")
    print()


except KeyboardInterrupt:

    print()
    print()
    print("==========================================")
    print("❌ KEYBOARD INTERRUPT DETECTED")
    print("==========================================")
    print()
    print("KeyboardInterrupt occurred while")
    print("Microphone InputStream was active.")
    print()
    print(f"Callbacks before interrupt: {callback_count}")
    print()


except Exception:

    print()
    print()
    print("==========================================")
    print("❌ MICROPHONE TEST ERROR")
    print("==========================================")
    print()

    traceback.print_exc()

    print()
    print("==========================================")


finally:

    print()
    print("[System] Microphone diagnostic finished.")
    
