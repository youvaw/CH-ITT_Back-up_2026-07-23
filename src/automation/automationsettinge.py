"""
=========================================
CHITT - Automation Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
from pathlib import Path


class AutomationSettings:

    def __init__(self):

        self.settings_file = Path(
            "automation/settings.json"
        )

        self.settings = {

            "enabled": True,

            "keyboard": {

                "delay": 0.05,

                "typing_speed": "normal"

            },

            "mouse": {

                "duration": 0.25,

                "failsafe": True

            },

            "scheduler": {

                "enabled": True,

                "check_interval": 30

            },

            "macro": {

                "enabled": True,

                "record_mouse": True,

                "record_keyboard": True

            },

            "clipboard": {

                "history_limit": 50

            },

            "safety": {

                "confirm_shutdown": True,

                "confirm_restart": True,

                "allow_delete": False

            },

            "paths": {

                "macro_folder": "automation/macros",

                "workflow_folder": "automation/workflows",

                "logs": "logs"

            }

        }

        self.load()

    # ---------------------------------
    # Load
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
    # Save
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
    # All
    # ---------------------------------

    def all(self):

        return self.settings

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "AutomationSettings",

            "status": "OK",

            "enabled": self.settings["enabled"]

        }


if __name__ == "__main__":

    settings = AutomationSettings()

    print(settings.health())

    print(settings.all())
