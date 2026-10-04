import threading
import time
import sounddevice as sd

result = {}

def worker():
    try:
        print("THREAD: START")

        wasapi = sd.WasapiSettings(auto_convert=True)

        print("WASAPI SETTINGS CREATED")

        stream = sd.InputStream(
            device=9,
            samplerate=48000,
            channels=2,
            dtype="float32",
            blocksize=3840,
            extra_settings=wasapi,
        )

        stream.start()

        print("WASAPI BACKGROUND STREAM: PASS")

        time.sleep(3)

        stream.stop()
        stream.close()

        print("WASAPI BACKGROUND STREAM CLOSED")

        result["pass"] = True

    except Exception as e:
        result["error"] = repr(e)
        print("ERROR:", repr(e))

print("=== EXPLICIT WASAPI BACKGROUND TEST ===")

t = threading.Thread(target=worker)
t.start()
t.join()

print("RESULT:", result)
print("=== TEST FINISHED ===")
