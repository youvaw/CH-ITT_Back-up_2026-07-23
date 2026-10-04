import time
import numpy as np
import sounddevice as sd
from openwakeword.model import Model

model = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx"
)

print("CHITT Wake Test Ready")
print("Say: HEY JARVIS")
print("Listening...")

def callback(indata, frames, time_info, status):
    audio = (indata[:, 0] * 32767).astype(np.int16)
    scores = model.predict(audio)
    score = scores.get("hey_jarvis", 0)

    if score > 0.5:
        print(f"WAKE WORD DETECTED! score={score:.3f}", flush=True)

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype="float32",
    blocksize=1280,
    device=1,
    callback=callback
):
    time.sleep(20)
