import os
import sys
import wave
import time

import sounddevice as sd
import numpy as np
from openwakeword.model import Model


# ==========================================
# CONFIG
# ==========================================

SAMPLE_RATE = 16000
DEVICE = 1
RECORD_SECONDS = 10
BLOCK_SIZE = 1280
THRESHOLD = 0.30

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ==========================================
# HEADER
# ==========================================

print("==========================================")
print("       MYX WAKE RECORD TEST")
print("==========================================")
print()

print("[Config]")
print(f"Device       : {DEVICE}")
print(f"Sample Rate  : {SAMPLE_RATE}")
print(f"Duration     : {RECORD_SECONDS}s")
print(f"Block Size   : {BLOCK_SIZE}")
print(f"Threshold    : {THRESHOLD}")
print()

# ==========================================
# LOAD MODEL
# ==========================================

print("[Wake] Loading HEY JARVIS model...")

model = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx"
)

print("[Wake] Model Ready")
print()

# ==========================================
# RECORD
# ==========================================

print("==========================================")
print("           🎤 RECORDING")
print("==========================================")
print()
print("First wait 2 seconds.")
print()
print("Then say:")
print()
print("HEY JARVIS")
print()
print("Say it clearly 2-3 times.")
print()
print("Recording will automatically stop.")
print("DO NOT PRESS CTRL+C")
print("==========================================")
print()

time.sleep(2)

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
print()

# ==========================================
# SIGNAL INFO
# ==========================================

audio_mono = audio[:, 0]

audio_float = audio_mono.astype(np.float32) / 32768.0

rms = float(
    np.sqrt(np.mean(audio_float ** 2))
)

max_value = float(
    np.max(np.abs(audio_float))
)

mean_abs = float(
    np.mean(np.abs(audio_float))
)

print("==========================================")
print("          RECORDING SIGNAL")
print("==========================================")
print(f"RMS        : {rms:.6f}")
print(f"MAX        : {max_value:.6f}")
print(f"MEAN ABS   : {mean_abs:.6f}")
print("==========================================")
print()

# ==========================================
# SAVE WAV
# ==========================================

filename = os.path.join(
    PROJECT_ROOT,
    "myx_wake_test.wav"
)

with wave.open(filename, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(audio_mono.tobytes())

print(f"[Audio] Saved:")
print(filename)
print()

# ==========================================
# RUN WAKE MODEL
# ==========================================

print("==========================================")
print("       🔍 ANALYZING RECORDING")
print("==========================================")
print()

best_score = 0.0
best_position = 0

chunk_count = 0

for start in range(
    0,
    len(audio_mono) - BLOCK_SIZE + 1,
    BLOCK_SIZE
):

    chunk = audio_mono[
        start:start + BLOCK_SIZE
    ]

    chunk_count += 1

    try:
        prediction = model.predict(chunk)

        score = float(
            prediction.get(
                "hey_jarvis",
                0.0
            )
        )

    except Exception as e:

        print("[Wake ERROR]")
        print(e)
        break

    if score > best_score:
        best_score = score
        best_position = start

    if score >= 0.05:
        print(
            f"[Wake] chunk={chunk_count:03d} "
            f"| score={score:.3f} "
            f"| best={best_score:.3f}"
        )

# ==========================================
# RESULTS
# ==========================================

print()
print("==========================================")
print("       WAKE RECORD TEST RESULTS")
print("==========================================")

print(f"Chunks analyzed : {chunk_count}")
print(f"Best score      : {best_score:.3f}")
print(f"Best position   : {best_position / SAMPLE_RATE:.2f}s")

print("==========================================")
print()

if best_score >= THRESHOLD:

    print("🔥 HEY JARVIS DETECTED")
    print("✅ Recorded audio contains a strong wake match.")

elif best_score >= 0.10:

    print("⚠️ Possible wake signal")
    print("Score is below detection threshold.")

else:

    print("❌ HEY JARVIS NOT DETECTED")
    print("Wake score is very low.")

print()
print("==========================================")
print("[System] Wake recording diagnostic finished.")
print("==========================================")

