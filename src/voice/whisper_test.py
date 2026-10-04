import sounddevice as sd
import tempfile
import wave

from faster_whisper import WhisperModel


# ==========================================
# MYX WHISPER SETTINGS
# ==========================================

SAMPLE_RATE = 16000
DEVICE = 1
RECORD_SECONDS = 5


# ==========================================
# LOAD WHISPER MODEL
# ==========================================

print("[Whisper] Loading BASE model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("[Whisper] Model Ready")
print()

# ==========================================
# START RECORDING
# ==========================================

print("==========================================")
print("       MYX VOICE → TEXT TEST")
print("==========================================")
print("🎤 Speak for 5 seconds...")
print("Example: Open Google Chrome")
print("==========================================")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16",
    device=DEVICE
)

sd.wait()

print()
print("[Whisper] Recording complete.")
print("[Whisper] Transcribing...")


# ==========================================
# SAVE AUDIO AS WAV
# ==========================================

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


# ==========================================
# TRANSCRIBE
# ==========================================

segments, info = model.transcribe(
    filename,
    language="en",
    beam_size=5,
    vad_filter=True
)


# ==========================================
# COLLECT TEXT
# ==========================================

text = ""

for segment in segments:
    text += segment.text


# ==========================================
# RESULT
# ==========================================

print()
print("==========================================")
print("📝 TRANSCRIPTION:")
print(text.strip())
print("==========================================")
print()

print(f"[Whisper] Detected language: {info.language}")
print(f"[Whisper] Language probability: {info.language_probability:.2f}")
