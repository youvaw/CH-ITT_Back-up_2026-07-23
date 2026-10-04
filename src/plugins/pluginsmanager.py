"""
CHITT Plugin Manager
"""

from .plugin_loader import PluginLoader


class PluginManager:

    def __init__(self):

        self.loader = PluginLoader()

        self.plugins = {}

    # ==========================================
    # Register
    # ==========================================

    def register(self, plugin):

        self.plugins[plugin.name] = plugin

    # ==========================================
    # Execute
    # ==========================================

    def execute(self, name, *args, **kwargs):

        plugin = self.plugins.get(name)

        if plugin:

            return plugin.execute(*args, **kwargs)

        raise Exception(f"Plugin '{name}' not found")

    # ==========================================
    # List
    # ==========================================

    def list(self):

        return list(self.plugins.keys())

    # ==========================================
    # Remove
    # ==========================================

    def remove(self, name):

        if name in self.plugins:

            del self.plugins[name]
 """
=========================================
CHITT - Plugin Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from plugins.plugin_loader import PluginLoader


class PluginManager:

    def __init__(self):

        self.loader = PluginLoader()

        self.plugins = {}

    # ---------------------------------
    # Load Plugins
    # ---------------------------------

    def load(self):

        self.plugins = self.loader.load()

        return self.plugins

    # ---------------------------------
    # Start All Plugins
    # ---------------------------------

    def start_all(self):

        for plugin in self.plugins.values():

            if plugin.is_enabled():

                try:

                    plugin.start()

                except Exception as error:

                    print(error)

    # ---------------------------------
    # Stop All Plugins
    # ---------------------------------

    def stop_all(self):

        for plugin in self.plugins.values():

            try:

                plugin.stop()

            except Exception as error:

                print(error)

    # ---------------------------------
    # Execute Plugin
    # ---------------------------------

    def execute(

        self,

        name,

        *args,

        **kwargs

    ):

        plugin = self.plugins.get(name)

        if plugin is None:

            raise ValueError(

                f"Plugin '{name}' not found."

            )

        if not plugin.is_enabled():

            raise RuntimeError(

                f"Plugin '{name}' is disabled."

            )

        return plugin.execute(

            *args,

            **kwargs

        )

    # ---------------------------------
    # Enable Plugin
    # ---------------------------------

    def enable(self, name):

        plugin = self.plugins.get(name)

        if plugin:

            plugin.enable()

            return True

        return False

    # ---------------------------------
    # Disable Plugin
    # ---------------------------------

    def disable(self, name):

        plugin = self.plugins.get(name)

        if plugin:

            plugin.disable()

            return True

        return False

    # ---------------------------------
    # Reload
    # ---------------------------------

    def reload(self):

        self.stop_all()

        self.plugins.clear()

        self.load()

        self.start_all()

    # ---------------------------------
    # Get Plugin
    # ---------------------------------

    def get(self, name):

        return self.plugins.get(name)

    # ---------------------------------
    # Plugin List
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
    # Status
    # ---------------------------------

    def status(self):

        result = {}

        for name, plugin in self.plugins.items():

            result[name] = plugin.health()

        return result

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return {

            "plugins": self.names(),

            "count": self.count()

        }


if __name__ == "__main__":

    manager = PluginManager()

    manager.load()

    manager.start_all()

    print(manager.info())
               
