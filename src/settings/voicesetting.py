"""
=========================================
CHITT - Voice Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from settings.settingsmanager import SettingsManager


class VoiceSettings:

    def __init__(self):

        self.settings = SettingsManager()

    # --------------------------
    # Voice
    # --------------------------

    def get_voice(self):

        return self.settings.get("voice")

    def set_voice(self, voice):

        self.settings.set("voice", voice)

    # --------------------------
    # Wake Word
    # --------------------------

    def get_wake_word(self):

        return self.settings.get("wake_word")

    def set_wake_word(self, wake_word):

        self.settings.set("wake_word", wake_word)

    # --------------------------
    # Voice Speed
    # --------------------------

    def get_speed(self):

        return self.settings.get("voice_speed")

    def set_speed(self, speed):

        self.settings.set("voice_speed", speed)

    # --------------------------
    # Volume
    # --------------------------

    def get_volume(self):

        return self.settings.get("volume")

    def set_volume(self, volume):

        if volume < 0:
            volume = 0

        if volume > 100:
            volume = 100

        self.settings.set("volume", volume)

    # --------------------------
    # Language
    # --------------------------

    def get_language(self):

        return self.settings.get("language")

    def set_language(self, language):

        self.settings.set("language", language)

    # --------------------------
    # Show Settings
    # --------------------------

    def show(self):

        print("Voice      :", self.get_voice())
        print("Wake Word  :", self.get_wake_word())
        print("Language   :", self.get_language())
        print("Speed      :", self.get_speed())
        print("Volume     :", self.get_volume())


if __name__ == "__main__":

    voice = VoiceSettings()

    voice.show()

