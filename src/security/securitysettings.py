"""
=========================================
CHITT - Security Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
from pathlib import Path


class SecuritySettings:

    def __init__(self):

        self.settings_file = Path(
            "security/settings.json"
        )

        self.settings = {

            "enabled": True,

            "security_level": "HIGH",

            "authentication": {

                "enabled": True,

                "max_attempts": 5,

                "session_timeout": 3600

            },

            "password": {

                "minimum_length": 8,

                "require_uppercase": True,

                "require_lowercase": True,

                "require_numbers": True,

                "require_symbols": True

            },

            "encryption": {

                "enabled": True,

                "algorithm": "Fernet"

            },

            "audit": {

                "enabled": True,

                "log_failed_login": True,

                "log_permission_changes": True

            },

            "permissions": {

                "default": "deny"

            }

        }

        self.load()

    # ---------------------------------
    # Load Settings
    # ---------------------------------

    def load(self):

        if self.settings_file.exists():

            with open(

                self.settings_file,

                "r",

                encoding="utf-8"

            ) as file:

                self.settings.update(

                    json.load(file)

                )

    # ---------------------------------
    # Save Settings
    # ---------------------------------

    def save(self):

        self.settings_file.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        with open(

            self.settings_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.settings,

                file,

                indent=4

            )

    # ---------------------------------
    # Get Setting
    # ---------------------------------

    def get(

        self,

        key,

        default=None

    ):

        return self.settings.get(

            key,

            default

        )

    # ---------------------------------
    # Set Setting
    # ---------------------------------

    def set(

        self,

        key,

        value

    ):

        self.settings[key] = value

        self.save()

    # ---------------------------------
    # Reset
    # ---------------------------------

    def reset(self):

        self.__init__()

        self.save()

    # ---------------------------------
    # All Settings
    # ---------------------------------

    def all(self):

        return self.settings

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "SecuritySettings",

            "enabled": self.settings["enabled"],

            "level": self.settings["security_level"],

            "status": "OK"

        }


if __name__ == "__main__":

    settings = SecuritySettings()

    print(settings.health())

    print(settings.all())
    
