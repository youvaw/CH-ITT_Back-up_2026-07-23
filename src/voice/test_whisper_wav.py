from faster_whisper import WhisperModel

WAV_FILE = "myx_last_command.wav"

print("==========================================")
print("        MYX WHISPER WAV TEST")
print("==========================================")

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe(
    WAV_FILE,
    language=None,
    beam_size=5,
    vad_filter=False,
    condition_on_previous_text=False
)

print(f"\nDetected language: {info.language}")
print(f"Language probability: {info.language_probability:.2f}")

print("\n--- TRANSCRIPTION ---")

text = ""

for segment in segments:
    print(f"[{segment.start:.2f} -> {segment.end:.2f}] {segment.text}")
    text += segment.text + " "

print("\nFINAL:")
print(text.strip())

print("\n==========================================")

