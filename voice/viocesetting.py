"""
CHITT Voice Settings
Author : AVISHKAR
"""

from settings.settings_manager import SettingsManager


class VoiceSettings:

    def __init__(self):

        self.settings = SettingsManager()

    def get_voice(self):

        return self.settings.get("voice")

    def set_voice(self, voice_name):

        self.settings.set("voice", voice_name)

    def get_speed(self):

        return self.settings.get("voice_speed")

    def set_speed(self, speed):

        self.settings.set("voice_speed", speed)

    def get_volume(self):

        return self.settings.get("volume")

    def set_volume(self, volume):

        self.settings.set("volume", volume)

    def speak_settings(self):

        print("Voice :", self.get_voice())
        print("Speed :", self.get_speed())
        print("Volume:", self.get_volume())


if __name__ == "__main__":

    voice = VoiceSettings()

    voice.speak_settings()

    voice.set_voice("female")

    voice.set_speed(200)

    voice.set_volume(90)

    print("\nUpdated Settings:\n")

    voice.speak_settings()

"""
=========================================
CHITT - Voice Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os


class VoiceSettings:

    def __init__(self):

        self.file_path = os.path.join(
            os.path.dirname(__file__),
            "voice_settings.json"
        )

        self.settings = {

            "voice": "default",

            "language": "en-US",

            "volume": 1.0,

            "speed": 180,

            "wake_word": "chitt",

            "microphone": "default",

            "speaker": "default"

        }

        self.load()

    # ---------------------------------
    # Load Settings
    # ---------------------------------

    def load(self):

        if os.path.exists(self.file_path):

            try:

                with open(
                    self.file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.settings.update(
                        json.load(file)
                    )

            except Exception:

                pass

    # ---------------------------------
    # Save Settings
    # ---------------------------------

    def save(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.settings,
                file,
                indent=4
            )

    # ---------------------------------
    # Voice
    # ---------------------------------

    def set_voice(self, voice):

        self.settings["voice"] = voice

        self.save()

    def get_voice(self):

        return self.settings["voice"]

    # ---------------------------------
    # Language
    # ---------------------------------

    def set_language(self, language):

        self.settings["language"] = language

        self.save()

    def get_language(self):

        return self.settings["language"]

    # ---------------------------------
    # Volume
    # ---------------------------------

    def set_volume(self, volume):

        self.settings["volume"] = volume

        self.save()

    def get_volume(self):

        return self.settings["volume"]

    # ---------------------------------
    # Speed
    # ---------------------------------

    def set_speed(self, speed):

        self.settings["speed"] = speed

        self.save()

    def get_speed(self):

        return self.settings["speed"]

    # ---------------------------------
    # Wake Word
    # ---------------------------------

    def set_wake_word(self, wake_word):

        self.settings["wake_word"] = wake_word

        self.save()

    def get_wake_word(self):

        return self.settings["wake_word"]

    # ---------------------------------
    # Microphone
    # ---------------------------------

    def set_microphone(self, mic):

        self.settings["microphone"] = mic

        self.save()

    def get_microphone(self):

        return self.settings["microphone"]

    # ---------------------------------
    # Speaker
    # ---------------------------------

    def set_speaker(self, speaker):

        self.settings["speaker"] = speaker

        self.save()

    def get_speaker(self):

        return self.settings["speaker"]

    # ---------------------------------
    # Get All
    # ---------------------------------

    def get_all(self):

        return self.settings

    # ---------------------------------
    # Reset
    # ---------------------------------

    def reset(self):

        if os.path.exists(self.file_path):

            os.remove(self.file_path)

        self.__init__()


if __name__ == "__main__":

    settings = VoiceSettings()

    print(settings.get_all())    
    