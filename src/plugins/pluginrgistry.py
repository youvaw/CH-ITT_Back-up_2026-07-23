"""
=========================================
CHITT - Plugin Registry
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from datetime import datetime


class PluginRegistry:

    def __init__(self):

        self.registry = {}

    # ---------------------------------
    # Register Plugin
    # ---------------------------------

    def register(self, plugin):

        self.registry[plugin.name] = {

            "plugin": plugin,

            "name": plugin.name,

            "version": plugin.version,

            "author": plugin.author,

            "description": plugin.description,

            "enabled": plugin.is_enabled(),

            "registered_at": datetime.now()

        }

        return True

    # ---------------------------------
    # Unregister Plugin
    # ---------------------------------

    def unregister(self, name):

        if name in self.registry:

            del self.registry[name]

            return True

        return False

    # ---------------------------------
    # Exists
    # ---------------------------------

    def exists(self, name):

        return name in self.registry

    # ---------------------------------
    # Get Plugin
    # ---------------------------------

    def get(self, name):

        if self.exists(name):

            return self.registry[name]["plugin"]

        return None

    # ---------------------------------
    # Metadata
    # ---------------------------------

    def metadata(self, name):

        if self.exists(name):

            data = self.registry[name].copy()

            data.pop("plugin")

            return data

        return None

    # ---------------------------------
    # List Plugins
    # ---------------------------------

    def plugins(self):

        return list(self.registry.keys())

    # ---------------------------------
    # Count
    # ---------------------------------

    def count(self):

        return len(self.registry)

    # ---------------------------------
    # Enable
    # ---------------------------------

    def enable(self, name):

        plugin = self.get(name)

        if plugin:

            plugin.enable()

            self.registry[name]["enabled"] = True

            return True

        return False

    # ---------------------------------
    # Disable
    # ---------------------------------

    def disable(self, name):

        plugin = self.get(name)

        if plugin:

            plugin.disable()

            self.registry[name]["enabled"] = False

            return True

        return False

    # ---------------------------------
    # Clear Registry
    # ---------------------------------

    def clear(self):

        self.registry.clear()

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return {

            "count": self.count(),

            "plugins": self.plugins()

        }


if __name__ == "__main__":

    registry = PluginRegistry()

    print(registry.info())
    
