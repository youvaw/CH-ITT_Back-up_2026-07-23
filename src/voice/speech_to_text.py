# -*- coding: utf-8 -*-

import os
import tempfile
import wave

import sounddevice as sd
from faster_whisper import WhisperModel


class SpeechToText:
    """
    MYX Speech-to-Text Service

    Features:
    - Whisper speech recognition
    - Automatic language detection
    - Marathi / Hindi / English support
    - Returns recognized text
    - Stores detected language and confidence
    """

    LANGUAGE_NAMES = {
        "en": "English",
        "hi": "Hindi",
        "mr": "Marathi",
    }

    def __init__(
        self,
        model_size="base",
        sample_rate=16000,
        device=1,
        record_seconds=5,
        language=None,
    ):
        print("[STT] Initializing...")

        self.model_size = model_size
        self.sample_rate = sample_rate
        self.device = device
        self.record_seconds = record_seconds

        # None = automatic language detection
        self.language = language

        # Latest detection information
        self.detected_language = None
        self.language_probability = 0.0
        self.last_text = ""

        self.model = WhisperModel(
            self.model_size,
            device="cpu",
            compute_type="int8",
        )

        print("[STT] Whisper Model Ready")
        print(f"[STT] Model: {self.model_size}")
        print(f"[STT] Microphone Device: {self.device}")
        print(f"[STT] Sample Rate: {self.sample_rate}")

        if self.language:
            print(f"[STT] Language Mode: {self.language}")
        else:
            print("[STT] Language Mode: AUTO")

    def listen(self):
        print("[STT] Listening...")

        filename = None

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
                language=self.language,
                beam_size=5,
                vad_filter=True,
            )

            # Save detected language information
            self.detected_language = getattr(
                info,
                "language",
                None,
            )

            self.language_probability = float(
                getattr(
                    info,
                    "language_probability",
                    0.0,
                )
            )

            text = "".join(
                segment.text
                for segment in segments
            ).strip()

            self.last_text = text

            language_name = self.LANGUAGE_NAMES.get(
                self.detected_language,
                self.detected_language or "Unknown",
            )

            print(
                f"[STT] Language: {language_name} "
                f"({self.language_probability:.2f})"
            )

            print(f"[STT] Result: {text}")

            return text

        except Exception as e:
            print(f"[STT ERROR] {e}")

            self.detected_language = None
            self.language_probability = 0.0
            self.last_text = ""

            return ""

        finally:
            if filename and os.path.exists(filename):
                try:
                    os.remove(filename)
                except Exception:
                    pass

    def get_language(self):
        """
        Return the latest detected language code.
        """
        return self.detected_language

    def get_language_name(self):
        """
        Return the latest detected language name.
        """
        return self.LANGUAGE_NAMES.get(
            self.detected_language,
            self.detected_language or "Unknown",
        )

    def get_language_probability(self):
        """
        Return the latest language detection confidence.
        """
        return self.language_probability

    def get_result(self):
        """
        Return the latest recognized text.
        """
        return self.last_text


if __name__ == "__main__":
    print("=" * 50)
    print("       MYX SPEECH TO TEXT TEST")
    print("=" * 50)

    stt = SpeechToText(
        model_size="base",
        sample_rate=48000,
        device=9,
        record_seconds=5,
        language=None,
    )

    text = stt.listen()

    print()
    print("=" * 50)
    print("Recognized Text:")
    print(text if text else "[No speech detected]")

    print()
    print("Detected Language:")
    print(stt.get_language_name())

    print()
    print("Language Code:")
    print(stt.get_language())

    print()
    print("Language Confidence:")
    print(f"{stt.get_language_probability():.2f}")

    print("=" * 50)
