"""
=========================================
CHITT - Settings Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os

# Safe Import: src.settings से import करें, fail होने पर fallback handle करें
try:
    from src.settings.defaults import DEFAULT_SETTINGS
except ModuleNotFoundError:
    try:
        from settings.defaults import DEFAULT_SETTINGS
    except ModuleNotFoundError:
        DEFAULT_SETTINGS = {}


class SettingsManager:

    def __init__(self):
        self.config_path = os.path.join(
            os.path.dirname(__file__),
            "config.json"
        )
        self.settings = {}
        self.load()

    def load(self):
        if not os.path.exists(self.config_path):
            self.settings = DEFAULT_SETTINGS.copy()
            self.save()
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                self.settings = json.load(file)
        except Exception:
            self.settings = DEFAULT_SETTINGS.copy()
            self.save()

    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump(
                self.settings,
                file,
                indent=4
            )

    def get(self, key):
        return self.settings.get(key)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def exists(self, key):
        return key in self.settings

    def remove(self, key):
        if key in self.settings:
            del self.settings[key]
            self.save()

    def reset(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.save()

    def get_all(self):
        return self.settings
    
