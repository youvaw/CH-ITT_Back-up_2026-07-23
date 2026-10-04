"""
CHITT AI
Configuration Loader
"""

"""
Resolve imports for both package layouts (top-level `config` or nested `src.config`).
This uses importlib to attempt importing the available module path so static
analyzers won't fail on the literal fallback import.
"""
import importlib

def _import_module_attr(module_paths, attr_name):
    for mod_path in module_paths:
        try:
            module = importlib.import_module(mod_path)
            return getattr(module, attr_name)
        except (ModuleNotFoundError, ImportError, AttributeError):
            continue
    raise ModuleNotFoundError(f"Could not import {attr_name} from any of: {module_paths}")

_settings_module_paths = ["config.settings", "src.config.settings"]
_environment_module_paths = ["config.environment", "src.config.environment"]

settings = _import_module_attr(_settings_module_paths, "settings")
CURRENT_ENVIRONMENT = _import_module_attr(_environment_module_paths, "CURRENT_ENVIRONMENT")
is_development = _import_module_attr(_environment_module_paths, "is_development")
is_testing = _import_module_attr(_environment_module_paths, "is_testing")
is_production = _import_module_attr(_environment_module_paths, "is_production")


class ConfigLoader:
    """Loads and provides application configuration."""

    def __init__(self):
        self.settings = settings
        self.environment = CURRENT_ENVIRONMENT

    def display(self):
        print("=" * 50)
        print("CHITT Configuration")
        print("=" * 50)
        print(f"App Name     : {self.settings.APP_NAME}")
        print(f"Version      : {self.settings.VERSION}")
        print(f"Author       : {self.settings.AUTHOR}")
        print(f"Environment  : {self.environment.value}")
        print(f"Debug Mode   : {self.settings.DEBUG}")
        print("=" * 50)


config = ConfigLoader()
"""
=========================================
CHITT - Voice Config Loader
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os

from voice.config import get_default_config


class ConfigLoader:

    def __init__(self):

        self.config_file = os.path.join(

            os.path.dirname(__file__),

            "voice_config.json"

        )

        self.config = get_default_config()

        self.load()

    # ---------------------------------
    # Load Configuration
    # ---------------------------------

    def load(self):

        if not os.path.exists(self.config_file):

            self.save()

            return self.config

        try:

            with open(

                self.config_file,

                "r",

                encoding="utf-8"

            ) as file:

                data = json.load(file)

                self.config.update(data)

        except Exception as error:

            print(

                "Config Load Error :",

                error

            )

        return self.config

    # ---------------------------------
    # Save Configuration
    # ---------------------------------

    def save(self):

        try:

            with open(

                self.config_file,

                "w",

                encoding="utf-8"

            ) as file:

                json.dump(

                    self.config,

                    file,

                    indent=4,

                    ensure_ascii=False

                )

        except Exception as error:

            print(

                "Config Save Error :",

                error

            )

    # ---------------------------------
    # Reload
    # ---------------------------------

    def reload(self):

        self.config = get_default_config()

        return self.load()

    # ---------------------------------
    # Get Value
    # ---------------------------------

    def get(self, key, default=None):

        return self.config.get(

            key,

            default

        )

    # ---------------------------------
    # Set Value
    # ---------------------------------

    def set(self, key, value):

        self.config[key] = value

        self.save()

    # ---------------------------------
    # Get All
    # ---------------------------------

    def get_all(self):

        return self.config

    # ---------------------------------
    # Reset Configuration
    # ---------------------------------

    def reset(self):

        self.config = get_default_config()

        self.save()

    # ---------------------------------
    # Exists
    # ---------------------------------

    def exists(self):

        return os.path.exists(

            self.config_file

        )


if __name__ == "__main__":

    loader = ConfigLoader()

    print(loader.get_all())
    