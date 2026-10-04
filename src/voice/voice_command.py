import os
import sys
import tempfile
import wave

import sounddevice as sd
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
# MYX COMPONENTS
# ============================================================

from src.core.brain import Brain
from src.core.router import CommandRouter


# ============================================================
# SETTINGS
# ============================================================

SAMPLE_RATE = 16000
DEVICE = 1
RECORD_SECONDS = 5


# ============================================================
# START
# ============================================================

print("==========================================")
print("       MYX VOICE COMMAND TEST")
print("==========================================")

print("[System] Starting Command Router...")
router = CommandRouter()

print("[System] Starting Brain...")
brain = Brain(self_router=router)

print("[Whisper] Loading BASE model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("[Whisper] Model Ready")

print()
print("==========================================")
print("🎤 Speak your command for 5 seconds")
print("==========================================")
print("Example:")
print("  Open Google")
print("  Open YouTube")
print("  Open Calculator")
print("  Open File Explorer")
print("==========================================")
print()


# ============================================================
# RECORD AUDIO
# ============================================================

print("[Mic] Recording...")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16",
    device=DEVICE
)

sd.wait()

print("[Mic] Recording complete.")


# ============================================================
# SAVE TEMP WAV
# ============================================================

with tempfile.NamedTemporaryFile(
    suffix=".wav",
    delete=False
) as temp:

    filename = temp.name


with wave.open(filename, "wb") as wf:

    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)

    wf.writeframes(audio.tobytes())


# ============================================================
# WHISPER TRANSCRIPTION
# ============================================================

print("[Whisper] Transcribing...")

segments, info = model.transcribe(
    filename,
    language="en",
    beam_size=5,
    vad_filter=True
)

text = ""

for segment in segments:
    text += segment.text


text = text.strip()


# ============================================================
# SHOW TEXT
# ============================================================

print()
print("==========================================")
print("📝 YOU SAID:")
print(text)
print("==========================================")

print()
print(f"[Whisper] Language: {info.language}")
print(f"[Whisper] Probability: {info.language_probability:.2f}")


# ============================================================
# SEND TO BRAIN
# ============================================================

if text:

    print()
    print("[Brain] Processing command...")

    response = brain.process(text)

    print()
    print("==========================================")
    print("🤖 MYX RESPONSE:")
    print(response)
    print("==========================================")

else:

    print()
    print("[Brain] No command detected.")


# ============================================================
# CLEAN TEMP FILE
# ============================================================

try:
    os.remove(filename)
except Exception:
    pass


print()
print("[System] Voice command test completed.")

