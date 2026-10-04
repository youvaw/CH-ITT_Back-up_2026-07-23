"""
=========================================
CHITT - Plugin Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os


class PluginSettings:

    SETTINGS_FILE = "plugins/plugin_settings.json"

    def __init__(self):

        self.settings = {}

        self.load()

    # ---------------------------------
    # Load Settings
    # ---------------------------------

    def load(self):

        if os.path.exists(self.SETTINGS_FILE):

            try:

                with open(

                    self.SETTINGS_FILE,

                    "r",

                    encoding="utf-8"

                ) as file:

                    self.settings = json.load(file)

            except Exception:

                self.settings = {}

        else:

            self.settings = {}

    # ---------------------------------
    # Save Settings
    # ---------------------------------

    def save(self):

        with open(

            self.SETTINGS_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.settings,

                file,

                indent=4

            )

    # ---------------------------------
    # Create Plugin Settings
    # ---------------------------------

    def create(

        self,

        plugin_name

    ):

        if plugin_name not in self.settings:

            self.settings[plugin_name] = {

                "enabled": True,

                "autoload": True,

                "permissions": [],

                "config": {}

            }

    # ---------------------------------
    # Get Setting
    # ---------------------------------

    def get(

        self,

        plugin_name,

        key,

        default=None

    ):

        self.create(plugin_name)

        return self.settings[plugin_name].get(

            key,

            default

        )

    # ---------------------------------
    # Set Setting
    # ---------------------------------

    def set(

        self,

        plugin_name,

        key,

        value

    ):

        self.create(plugin_name)

        self.settings[plugin_name][key] = value

    # ---------------------------------
    # Enable Plugin
    # ---------------------------------

    def enable(

        self,

        plugin_name

    ):

        self.set(

            plugin_name,

            "enabled",

            True

        )

    # ---------------------------------
    # Disable Plugin
    # ---------------------------------

    def disable(

        self,

        plugin_name

    ):

        self.set(

            plugin_name,

            "enabled",

            False

        )

    # ---------------------------------
    # Remove Plugin Settings
    # ---------------------------------

    def remove(

        self,

        plugin_name

    ):

        if plugin_name in self.settings:

            del self.settings[plugin_name]

    # ---------------------------------
    # Plugin List
    # ---------------------------------

    def plugins(self):

        return list(

            self.settings.keys()

        )

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return {

            "plugins": self.plugins(),

            "count": len(self.settings)

        }


if __name__ == "__main__":

    settings = PluginSettings()

    settings.create("WeatherPlugin")

    settings.enable("WeatherPlugin")

    settings.save()

    print(settings.info())
    
