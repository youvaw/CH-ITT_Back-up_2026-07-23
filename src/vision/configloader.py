"""
=========================================
CHITT - Vision Config Loader
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os

from vision.config import CONFIG_PATH


class ConfigLoader:

    def __init__(self):

        self.config = {}

        self.path = CONFIG_PATH

    # -----------------------------
    # Load Config
    # -----------------------------

    def load(self):

        if not os.path.exists(self.path):

            self.config = {}

            return self.config

        with open(

            self.path,

            "r",

            encoding="utf-8"

        ) as file:

            self.config = json.load(file)

        return self.config

    # -----------------------------
    # Save Config
    # -----------------------------

    def save(self):

        with open(

            self.path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.config,

                file,

                indent=4

            )

    # -----------------------------
    # Get Value
    # -----------------------------

    def get(self, key, default=None):

        return self.config.get(

            key,

            default

        )

    # -----------------------------
    # Set Value
    # -----------------------------

    def set(self, key, value):

        self.config[key] = value

    # -----------------------------
    # Remove Key
    # -----------------------------

    def remove(self, key):

        if key in self.config:

            del self.config[key]

    # -----------------------------
    # Clear Config
    # -----------------------------

    def clear(self):

        self.config.clear()

    # -----------------------------
    # Reload
    # -----------------------------

    def reload(self):

        return self.load()

    # -----------------------------
    # Config Info
    # -----------------------------

    def info(self):

        return {

            "path": self.path,

            "keys": len(self.config)

        }


if __name__ == "__main__":

    loader = ConfigLoader()

    loader.load()

    print(loader.info())
    
