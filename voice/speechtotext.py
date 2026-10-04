"""
CHITT Speech To Text Engine
"""

import speech_recognition as sr

from .config import (
    WAKE_WORDS,
    DEFAULT_LANGUAGE,
    LISTEN_TIMEOUT,
    PHRASE_TIMEOUT,
    ENERGY_THRESHOLD,
)


class SpeechToText:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.recognizer.energy_threshold = ENERGY_THRESHOLD

        self.recognizer.dynamic_energy_threshold = True

    def listen(self):

        with sr.Microphone() as source:

            print("🎤 Listening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = self.recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=PHRASE_TIMEOUT,
            )

        return audio

    def recognize(self, audio):

        try:

            text = self.recognizer.recognize_google(
                audio,
                language=DEFAULT_LANGUAGE,
            )

            print("You :", text)

            return text.lower()

        except sr.UnknownValueError:

            return ""

        except sr.RequestError:

            print("Speech Service Unavailable")

            return ""

    def wait_for_wake_word(self):

        print("Waiting for CHITT...")

        while True:

            audio = self.listen()

            text = self.recognize(audio)

            for word in WAKE_WORDS:

                if word in text:

                    print(f"Wake Word Detected : {word}")

                    return True


if __name__ == "__main__":

    stt = SpeechToText()

    stt.wait_for_wake_word()

    audio = stt.listen()

    text = stt.recognize(audio)

    print(text)
    