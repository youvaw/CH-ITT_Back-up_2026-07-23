import os
import sys
import time
import traceback

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
# CONFIG
# ==========================================

TEST_DELAY = 2


# ==========================================
# HEADER
# ==========================================

print("==========================================")
print("          MYX TTS LISTENER TEST")
print("==========================================")
print()

print("[Test]")
print("This test contains:")
print("✅ TTS")
print("✅ Python main thread")
print()
print("This test DOES NOT contain:")
print("❌ Microphone")
print("❌ OpenWakeWord")
print("❌ Whisper")
print("❌ Brain")
print("❌ Command Router")
print("❌ Threads")
print("❌ InputStream")
print()

# ==========================================
# INITIALIZE TTS
# ==========================================

print("[TTS] Initializing...")

try:
    tts = MyXTTS()
    print("[TTS] Engine Ready")

except Exception:
    print()
    print("==========================================")
    print("       ❌ TTS INITIALIZATION ERROR")
    print("==========================================")
    traceback.print_exc()
    sys.exit(1)


# ==========================================
# TTS TEST 1
# ==========================================

try:
    print()
    print("==========================================")
    print("           TTS TEST 1")
    print("==========================================")

    print("[TTS] Speaking...")
    
    tts.speak(
        "Yes, how can I help?"
    )

    print("[TTS] Speaking finished.")

except Exception:
    print()
    print("==========================================")
    print("             ❌ TTS ERROR")
    print("==========================================")
    traceback.print_exc()


# ==========================================
# WAIT
# ==========================================

print()
print(f"[System] Waiting {TEST_DELAY} seconds...")
time.sleep(TEST_DELAY)


# ==========================================
# TTS TEST 2
# ==========================================

try:
    print()
    print("==========================================")
    print("           TTS TEST 2")
    print("==========================================")

    print("[TTS] Speaking again...")

    tts.speak(
        "MyX voice system is working correctly."
    )

    print("[TTS] Second response finished.")

except Exception:
    print()
    print("==========================================")
    print("             ❌ TTS ERROR")
    print("==========================================")
    traceback.print_exc()


# ==========================================
# WAIT
# ==========================================

print()
print(f"[System] Waiting {TEST_DELAY} seconds...")
time.sleep(TEST_DELAY)


# ==========================================
# FINAL TEST
# ==========================================

try:
    print()
    print("==========================================")
    print("          TTS FINAL TEST")
    print("==========================================")

    print("[TTS] Final response...")

    tts.speak(
        "Hello Avishkar. I am MyX. TTS is ready."
    )

    print("[TTS] Final response finished.")

except Exception:
    print()
    print("==========================================")
    print("             ❌ TTS ERROR")
    print("==========================================")
    traceback.print_exc()


# ==========================================
# CLEANUP
# ==========================================

print()
print("[TTS] Stopping engine...")

try:
    tts.stop()
except Exception as e:
    print(f"[TTS Stop Warning] {e}")


# ==========================================
# RESULTS
# ==========================================

print()
print("==========================================")
print("          MYX TTS TEST COMPLETE")
print("==========================================")
print()
print("If all three responses were spoken:")
print("✅ TTS ENGINE WORKS")
print("✅ Multiple speak() calls work")
print("✅ TTS does not cause KeyboardInterrupt")
print()
print("==========================================")
print("[System] TTS diagnostic finished.")
print("==========================================")

