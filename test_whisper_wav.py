from faster_whisper import WhisperModel
import os

WAV_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "myx_last_command.wav"
)

print("==========================================")
print("        MYX WHISPER WAV TEST")
print("==========================================")

print(f"[Audio] File: {WAV_FILE}")

if not os.path.exists(WAV_FILE):
    print("\nERROR: myx_last_command.wav not found!")
    print("First run voice_assistant.py and speak a command.")
    input("\nPress Enter to exit...")
    raise SystemExit

print(f"[Audio] File found: {os.path.getsize(WAV_FILE)} bytes")

print("\n[Whisper] Loading tiny model...")

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

print("[Whisper] Model ready.")
print("[Whisper] Transcribing saved WAV...\n")

segments, info = model.transcribe(
    WAV_FILE,
    language=None,
    beam_size=5,
    vad_filter=False,
    condition_on_previous_text=False
)

print("==========================================")
print(f"Detected language : {info.language}")
print(f"Language probability: {info.language_probability:.2f}")
print("==========================================")

full_text = []

for segment in segments:
    text = segment.text.strip()

    if text:
        print(
            f"[{segment.start:.2f}s -> {segment.end:.2f}s] "
            f"{text}"
        )
        full_text.append(text)

final_text = " ".join(full_text).strip()

print("\n==========================================")
print("FINAL TRANSCRIPTION")
print("==========================================")

if final_text:
    print(final_text)
else:
    print("(No speech detected)")

print("==========================================")

input("\nPress Enter to exit...")
