"""
CHITT AI
Configuration Manager
"""

import json
from pathlib import Path


class ConfigManager:

    def __init__(self):

        config_path = (
            Path(__file__).parent / "settings.json"
        )

        with open(config_path, "r", encoding="utf-8") as file:

            self.config = json.load(file)

    def get(self, key, default=None):

        return self.config.get(key, default)

    def set(self, key, value):

        self.config[key] = value

    def save(self):

        config_path = (
            Path(__file__).parent / "settings.json"
        )

        with open(config_path, "w", encoding="utf-8") as file:

            json.dump(
                self.config,
                file,
                indent=4
            )
"""
=========================================
CHITT - Voice Config Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from voice.config_loader import ConfigLoader


class ConfigManager:

    def __init__(self):

        self.loader = ConfigLoader()

    # ---------------------------------
    # Get Config
    # ---------------------------------

    def get(self, key):

        return self.loader.get(key)

    # ---------------------------------
    # Set Config
    # ---------------------------------

    def set(self, key, value):

        self.loader.set(key, value)

    # ---------------------------------
    # Voice
    # ---------------------------------

    def set_voice(self, voice):

        self.set("voice", voice)

    def get_voice(self):

        return self.get("voice")

    # ---------------------------------
    # Language
    # ---------------------------------

    def set_language(self, language):

        self.set("language", language)

    def get_language(self):

        return self.get("language")

    # ---------------------------------
    # Volume
    # ---------------------------------

    def set_volume(self, volume):

        self.set("volume", volume)

    def get_volume(self):

        return self.get("volume")

    # ---------------------------------
    # Speed
    # ---------------------------------

    def set_speed(self, speed):

        self.set("rate", speed)

    def get_speed(self):

        return self.get("rate")

    # ---------------------------------
    # Wake Word
    # ---------------------------------

    def set_wake_word(self, wake_word):

        self.set("wake_word", wake_word)

    def get_wake_word(self):

        return self.get("wake_word")

    # ---------------------------------
    # Debug
    # ---------------------------------

    def enable_debug(self):

        self.set("debug", True)

    def disable_debug(self):

        self.set("debug", False)

    def is_debug(self):

        return self.get("debug")

    # ---------------------------------
    # Get All Config
    # ---------------------------------

    def get_all(self):

        return self.loader.get_all()

    # ---------------------------------
    # Reload Config
    # ---------------------------------

    def reload(self):

        return self.loader.reload()

    # ---------------------------------
    # Reset Config
    # ---------------------------------

    def reset(self):

        self.loader.reset()

    # ---------------------------------
    # Save
    # ---------------------------------

    def save(self):

        self.loader.save()


if __name__ == "__main__":

    config = ConfigManager()

    print(config.get_all())
    
            