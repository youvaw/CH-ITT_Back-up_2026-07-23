import sounddevice as sd
import numpy as np
from openwakeword.model import Model
from faster_whisper import WhisperModel

print("CHITT NEW VOICE PIPELINE")
print("Loading wake word...")

wake = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx"
)

print("Loading Whisper...")
whisper = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

print("READY")
print("Say: HEY JARVIS")

audio = sd.rec(
    int(16000 * 5),
    samplerate=16000,
    channels=1,
    dtype="float32",
    device=1
)

sd.wait()

data = (audio[:, 0] * 32767).astype(np.int16)

scores = wake.predict(data)

print("WAKE SCORES:", scores)

segments, info = whisper.transcribe(
    audio[:, 0],
    language="en"
)

text = " ".join(segment.text for segment in segments).strip()

print("HEARD:", text)
print("CHITT PIPELINE TEST = COMPLETE")
