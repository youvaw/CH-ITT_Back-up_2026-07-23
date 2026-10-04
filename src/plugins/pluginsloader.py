"""
CHITT Plugin Loader
"""

import importlib
import pkgutil


class PluginLoader:

    def __init__(self):

        self.plugins = {}

    # ==========================================
    # Load Plugins
    # ==========================================

    def load(self, package):

        self.plugins.clear()

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):

            module = importlib.import_module(

                f"{package.__name__}.{module_name}"

            )

            if hasattr(module, "Plugin"):

                plugin = module.Plugin()

                self.plugins[plugin.name] = plugin

        return self.plugins

    # ==========================================
    # Get Loaded Plugins
    # ==========================================

    def get_plugins(self):

        return self.plugins
"""
=========================================
CHITT - Plugin Loader
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import importlib
import inspect

from plugins.plugin_base import PluginBase


class PluginLoader:

    def __init__(self):

        self.plugin_path = "plugins"

        self.plugins = {}

    # ---------------------------------
    # Load Plugins
    # ---------------------------------

    def load(self):

        for file in os.listdir(self.plugin_path):

            if not file.endswith(".py"):

                continue

            if file.startswith("__"):

                continue

            if file in [

                "plugin_base.py",

                "plugin_loader.py",

                "plugin_manager.py",

                "plugin_registry.py",

                "plugin_settings.py",

                "environment.py"

            ]:

                continue

            module_name = file[:-3]

            try:

                module = importlib.import_module(

                    f"plugins.{module_name}"

                )

                self.register(module)

            except Exception as error:

                print(

                    f"Plugin Error : "

                    f"{module_name}"

                )

                print(error)

        return self.plugins

    # ---------------------------------
    # Register Plugin
    # ---------------------------------

    def register(self, module):

        for _, obj in inspect.getmembers(

            module,

            inspect.isclass

        ):

            if (

                issubclass(obj, PluginBase)

                and obj != PluginBase

            ):

                plugin = obj()

                self.plugins[

                    plugin.name

                ] = plugin

                print(

                    f"Loaded : "

                    f"{plugin.name}"

                )

    # ---------------------------------
    # Get Plugin
    # ---------------------------------

    def get(self, name):

        return self.plugins.get(name)

    # ---------------------------------
    # List Plugins
    # ---------------------------------

    def names(self):

        return list(

            self.plugins.keys()

        )

    # ---------------------------------
    # Count
    # ---------------------------------

    def count(self):

        return len(

            self.plugins

        )

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return {

            "count": self.count(),

            "plugins": self.names()

        }


if __name__ == "__main__":

    loader = PluginLoader()

    loader.load()

    print(loader.info())
        
