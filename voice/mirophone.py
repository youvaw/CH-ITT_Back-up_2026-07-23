"""
=========================================
CHITT - Microphone
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import speech_recognition as sr


class Microphone:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.microphone = sr.Microphone()

    # ---------------------------------
    # Listen
    # ---------------------------------

    def listen(self):

        with self.microphone as source:

            print("🎤 Listening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = self.recognizer.listen(source)

            return audio

    # ---------------------------------
    # Noise Adjustment
    # ---------------------------------

    def adjust_noise(self):

        with self.microphone as source:

            self.recognizer.adjust_for_ambient_noise(source)

    # ---------------------------------
    # Get Recognizer
    # ---------------------------------

    def get_recognizer(self):

        return self.recognizer

    # ---------------------------------
    # Get Microphone
    # ---------------------------------

    def get_microphone(self):

        return self.microphone


if __name__ == "__main__":

    mic = Microphone()

    audio = mic.listen()

    print("Audio Captured Successfully.")
    