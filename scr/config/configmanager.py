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

            