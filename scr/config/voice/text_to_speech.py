"""
CHITT Text To Speech
"""

import pyttsx3


class TextToSpeech:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 180)

    def speak(self, text):

        print("CHITT :", text)

        self.engine.say(text)

        self.engine.runAndWait()
        