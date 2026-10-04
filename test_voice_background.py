import threading
import time
from src.voice.voice_engine import MyXVoiceEngine

result = {}

def worker():
    try:
        engine = MyXVoiceEngine(brain=None)
        result["engine"] = engine
        engine.start()
    except Exception as e:
        result["error"] = repr(e)

print("=== CLEAN BACKGROUND VOICE TEST ===")

thread = threading.Thread(target=worker, daemon=True)
thread.start()

time.sleep(8)

print("THREAD ALIVE:", thread.is_alive())
print("ERROR:", result.get("error"))

if "engine" in result:
    print("ENGINE CREATED: YES")
    result["engine"].stop()

thread.join(timeout=3)

print("=== TEST FINISHED ===")
