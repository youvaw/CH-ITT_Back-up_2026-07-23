# -*- coding: utf-8 -*-

import os
import tempfile
import wave

import sounddevice as sd
from faster_whisper import WhisperModel


class SpeechToText:
    """
    MYX Speech-to-Text Service

    Records microphone audio and converts it to text
    using Faster-Whisper.
    """

    def __init__(
        self,
        model_size="base",
        sample_rate=16000,
        device=1,
        record_seconds=5,
    ):
        print("[STT] Initializing...")

        self.model_size = model_size
        self.sample_rate = sample_rate
        self.device = device
        self.record_seconds = record_seconds

        self.model = WhisperModel(
            self.model_size,
            device="cpu",
            compute_type="int8",
        )

        print("[STT] Whisper Model Ready")
        print(f"[STT] Model: {self.model_size}")
        print(f"[STT] Microphone Device: {self.device}")
        print(f"[STT] Sample Rate: {self.sample_rate}")

    def listen(self):
        """
        Record audio and return recognized text.
        """

        print("[STT] Listening...")

        try:
            audio = sd.rec(
                int(self.record_seconds * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16",
                device=self.device,
            )

            sd.wait()

            print("[STT] Recording complete.")
            print("[STT] Transcribing...")

            filename = None

            try:
                with tempfile.NamedTemporaryFile(
                    suffix=".wav",
                    delete=False,
                ) as temp:
                    filename = temp.name

                with wave.open(filename, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(audio.tobytes())

                segments, info = self.model.transcribe(
                    filename,
                    language="en",
                    beam_size=5,
                    vad_filter=False,
                )

                text = "".join(
                    segment.text
                    for segment in segments
                ).strip()

                print(f"[STT] Result: {text}")

                return text

            finally:
                if filename and os.path.exists(filename):
                    try:
                        os.remove(filename)
                    except Exception:
                        pass

        except Exception as e:
            print(f"[STT ERROR] {e}")
            return ""

    def transcribe(self, audio_file):
        """
        Transcribe an existing WAV/audio file.
        """

        try:
            segments, info = self.model.transcribe(
                audio_file,
                language="en",
                beam_size=5,
                vad_filter=True,
            )

            return "".join(
                segment.text
                for segment in segments
            ).strip()

        except Exception as e:
            print(f"[STT ERROR] {e}")
            return ""


if __name__ == "__main__":
    print("=" * 50)
    print("        MYX SPEECH TO TEXT TEST")
    print("=" * 50)

    stt = SpeechToText()

    text = stt.listen()

    print()
    print("=" * 50)
    print("Recognized Text:")
    print(text if text else "[No speech detected]")
    print("=" * 50)
   