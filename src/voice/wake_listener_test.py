# -*- coding: utf-8 -*-

import queue
import threading
import time
import traceback

import numpy as np
import sounddevice as sd
from scipy.signal import resample_poly
from openwakeword.model import Model


# ============================================================
# MYX FINAL LIVE WAKE PIPELINE
#
# WASAPI 48 kHz
#       ↓
# Raw continuous audio
#       ↓
# 48 kHz → 16 kHz
#       ↓
# Continuous 16 kHz buffer
#       ↓
# 1280-sample chunks
#       ↓
# OpenWakeWord
# ============================================================


INPUT_SAMPLE_RATE = 48000
WAKE_SAMPLE_RATE = 16000

DEVICE = 9

INPUT_BLOCK_SIZE = 3840
WAKE_BLOCK_SIZE = 1280

TEST_SECONDS = 15

WAKE_THRESHOLD = 0.35


# ============================================================
# QUEUE / STATE
# ============================================================

audio_queue = queue.Queue(maxsize=30)

running = True

callback_count = 0
processed_blocks = 0
detection_count = 0

best_score = 0.0
best_peak = 0.0
best_rms = 0.0


# ============================================================
# MODEL
# ============================================================

print("=" * 60)
print("        MYX FINAL LIVE WAKE TEST")
print("=" * 60)

print(f"Device            : {DEVICE}")
print(f"Input Rate        : {INPUT_SAMPLE_RATE} Hz")
print(f"Wake Rate         : {WAKE_SAMPLE_RATE} Hz")
print(f"Input Block       : {INPUT_BLOCK_SIZE}")
print(f"Wake Block        : {WAKE_BLOCK_SIZE}")
print(f"Threshold         : {WAKE_THRESHOLD}")
print(f"Duration          : {TEST_SECONDS}s")

print("=" * 60)
print()

print("[Wake] Loading HEY JARVIS model...")

model = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx"
)

print("[Wake] Model loaded successfully.")


# ============================================================
# MICROPHONE CALLBACK
# ============================================================

def audio_callback(indata, frames, time_info, status):

    global callback_count

    callback_count += 1

    if status:
        print(f"[Mic Status] {status}")

    try:

        audio = (
            indata[:, 0]
            .astype(np.float32)
            .copy()
        )

        # IMPORTANT:
        # Keep microphone audio RAW.
        # No gain.
        # No per-block normalization.
        # No DC removal.

        try:

            audio_queue.put_nowait(audio)

        except queue.Full:

            print(
                "[Queue] Warning: audio queue full."
            )

    except Exception as e:

        print(
            f"[Callback ERROR] {e}"
        )


# ============================================================
# INFERENCE WORKER
# ============================================================

def inference_worker():

    global processed_blocks
    global detection_count
    global best_score
    global best_peak
    global best_rms

    print("[Worker] Started.")

    # Continuous 16 kHz audio buffer.
    wake_buffer = np.empty(
        0,
        dtype=np.float32
    )

    while running:

        try:

            audio_48k = audio_queue.get(
                timeout=0.2
            )

        except queue.Empty:

            continue

        try:

            # ==================================================
            # RAW AUDIO METRICS
            # ==================================================

            peak = float(
                np.max(
                    np.abs(audio_48k)
                )
            )

            rms = float(
                np.sqrt(
                    np.mean(
                        audio_48k * audio_48k
                    )
                )
            )

            best_peak = max(
                best_peak,
                peak
            )

            best_rms = max(
                best_rms,
                rms
            )

            # ==================================================
            # RESAMPLE
            #
            # 3840 samples @ 48k
            #          ↓
            # 1280 samples @ 16k
            # ==================================================

            audio_16k = resample_poly(
                audio_48k,
                WAKE_SAMPLE_RATE,
                INPUT_SAMPLE_RATE
            ).astype(np.float32)

            # ==================================================
            # CONTINUOUS BUFFER
            # ==================================================

            wake_buffer = np.concatenate(
                (
                    wake_buffer,
                    audio_16k
                )
            )

            # ==================================================
            # PROCESS EXACT 1280-SAMPLE CHUNKS
            # ==================================================

            while len(wake_buffer) >= WAKE_BLOCK_SIZE:

                chunk = wake_buffer[
                    :WAKE_BLOCK_SIZE
                ]

                wake_buffer = wake_buffer[
                    WAKE_BLOCK_SIZE:
                ]

                # ----------------------------------------------
                # Keep exactly the same amplitude relationship
                # as the successful offline WAV test.
                # ----------------------------------------------

                chunk = np.clip(
                    chunk,
                    -1.0,
                    1.0
                )

                pcm16 = (
                    chunk * 32767.0
                ).astype(np.int16)

                # ==================================================
                # OPENWAKEWORD
                # ==================================================

                prediction = model.predict(
                    pcm16
                )

                score = float(
                    prediction.get(
                        "hey_jarvis",
                        0.0
                    )
                )

                processed_blocks += 1

                if score > best_score:
                    best_score = score

                # ==================================================
                # DEBUG
                # ==================================================

                if processed_blocks % 25 == 0:

                    print(
                        f"[Wake] "
                        f"blocks={processed_blocks} "
                        f"| peak={peak:.3f} "
                        f"| rms={rms:.3f} "
                        f"| score={score:.4f} "
                        f"| best={best_score:.4f}"
                    )

                # ==================================================
                # DETECTION
                # ==================================================

                if score >= WAKE_THRESHOLD:

                    detection_count += 1

                    print()
                    print("=" * 60)
                    print("          ★ HEY JARVIS DETECTED ★")
                    print("=" * 60)

                    print(
                        f"Wake Score : {score:.4f}"
                    )

                    print(
                        f"Audio Peak : {peak:.4f}"
                    )

                    print(
                        f"Audio RMS  : {rms:.4f}"
                    )

                    print(
                        f"Detection  : #{detection_count}"
                    )

                    print("=" * 60)
                    print()

        except Exception as e:

            print(
                f"[Worker ERROR] {e}"
            )


# ============================================================
# START WORKER
# ============================================================

worker = threading.Thread(
    target=inference_worker,
    daemon=True
)

worker.start()


# ============================================================
# START MICROPHONE
# ============================================================

print()
print("[Mic] Opening WASAPI InputStream...")

start_time = time.monotonic()

try:

    with sd.InputStream(
        samplerate=INPUT_SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=DEVICE,
        blocksize=INPUT_BLOCK_SIZE,
        callback=audio_callback
    ):

        print("[Mic] InputStream OPEN")

        print()
        print("=" * 60)
        print("       MYX WAKE LISTENER ACTIVE")
        print("=" * 60)

        print()
        print("Say clearly:")
        print()
        print("              HEY JARVIS")
        print()

        print("Pipeline:")
        print()
        print("  WASAPI 48 kHz")
        print("       ↓")
        print("  RAW AUDIO")
        print("       ↓")
        print("  48 → 16 kHz")
        print("       ↓")
        print("  CONTINUOUS BUFFER")
        print("       ↓")
        print("  1280 SAMPLE CHUNKS")
        print("       ↓")
        print("  OPENWAKEWORD")
        print()

        print("Brain : OFF")
        print("STT   : OFF")
        print("TTS   : OFF")
        print("GUI   : OFF")
        print()

        print("=" * 60)

        while (
            time.monotonic() - start_time
            < TEST_SECONDS
        ):

            elapsed = int(
                time.monotonic() - start_time
            )

            remaining = (
                TEST_SECONDS - elapsed
            )

            print(
                f"\r[Timer] {remaining:02d}s remaining...",
                end="",
                flush=True
            )

            time.sleep(1)


except KeyboardInterrupt:

    print()
    print("[System] Interrupted.")


except Exception:

    print()
    print("=" * 60)
    print("          INPUT STREAM ERROR")
    print("=" * 60)

    traceback.print_exc()


finally:

    running = False

    print()
    print()
    print("=" * 60)
    print("             FINAL RESULTS")
    print("=" * 60)

    print(
        f"Callbacks        : {callback_count}"
    )

    print(
        f"Processed Blocks : {processed_blocks}"
    )

    print(
        f"Detections       : {detection_count}"
    )

    print(
        f"Best Wake Score  : {best_score:.4f}"
    )

    print(
        f"Best Audio Peak  : {best_peak:.4f}"
    )

    print(
        f"Best Audio RMS   : {best_rms:.4f}"
    )

    print("=" * 60)

    if detection_count > 0:

        print()
        print("✅ WAKE PIPELINE PASS")
        print()
        print(
            "HEY JARVIS detection is working."
        )
        print()
        print(
            "NEXT: integrate this pipeline "
            "into voice_engine.py"
        )

    else:

        print()
        print("❌ WAKE PIPELINE NOT PASS")
        print()
        print(
            "Do not change threshold yet."
        )

    print()
    print("[System] Final live wake test finished.")
    