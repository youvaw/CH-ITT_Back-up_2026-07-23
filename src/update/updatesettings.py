"""
=========================================
CHITT - Update Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
from pathlib import Path


class UpdateSettings:

    def __init__(self):

        self.settings_file = Path(
            "update_system/settings.json"
        )

        self.settings = {

            "enabled": True,

            "auto_update": False,

            "channel": "stable",

            "check_interval_hours": 24,

            "download_directory": "downloads",

            "backup_before_update": True,

            "rollback_on_failure": True,

            "notify_before_update": True,

            "notify_after_update": True,

            "verify_checksum": True

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
    # Get
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
    # Set
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

            "module": "UpdateSettings",

            "enabled": self.settings["enabled"],

            "channel": self.settings["channel"],

            "status": "OK"

        }


if __name__ == "__main__":

    settings = UpdateSettings()

    print(settings.health())

    print(settings.all())
    
