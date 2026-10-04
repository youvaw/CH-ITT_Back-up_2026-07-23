"""
=========================================
CHITT - Voice Utilities
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import speech_recognition as sr
import pyttsx3


class VoiceUtils:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.recognizer = sr.Recognizer()

    # ---------------------------------
    # Check Microphone
    # ---------------------------------

    def microphone_available(self):

        try:

            sr.Microphone()

            return True

        except Exception:

            return False

    # ---------------------------------
    # Check Speaker
    # ---------------------------------

    def speaker_available(self):

        try:

            self.engine.say("")

            return True

        except Exception:

            return False

    # ---------------------------------
    # Get Voices
    # ---------------------------------

    def get_voices(self):

        voices = self.engine.getProperty("voices")

        result = []

        for index, voice in enumerate(voices):

            result.append({

                "id": index,

                "name": voice.name,

                "voice_id": voice.id

            })

        return result

    # ---------------------------------
    # Get Current Rate
    # ---------------------------------

    def get_rate(self):

        return self.engine.getProperty("rate")

    # ---------------------------------
    # Get Current Volume
    # ---------------------------------

    def get_volume(self):

        return self.engine.getProperty("volume")

    # ---------------------------------
    # Supported Languages
    # ---------------------------------

    def supported_languages(self):

        return [

            "en-US",

            "en-IN",

            "hi-IN"

        ]

    # ---------------------------------
    # Voice Information
    # ---------------------------------

    def info(self):

        return {

            "microphone": self.microphone_available(),

            "speaker": self.speaker_available(),

            "voices": len(self.get_voices()),

            "rate": self.get_rate(),

            "volume": self.get_volume()

        }

    # ---------------------------------
    # Show Information
    # ---------------------------------

    def show(self):

        data = self.info()

        print("\n===== VOICE INFO =====\n")

        for key, value in data.items():

            print(f"{key} : {value}")


if __name__ == "__main__":

    utils = VoiceUtils()

    utils.show()
    