"""
CHITT Speech To Text
"""

import speech_recognition as sr


class SpeechToText:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):

        with sr.Microphone() as source:

            print("Listening...")

            self.recognizer.adjust_for_ambient_noise(source)

            audio = self.recognizer.listen(source)

        try:

            return self.recognizer.recognize_google(audio) # pyright: ignore[reportAttributeAccessIssue]

        except Exception:

            return None
        