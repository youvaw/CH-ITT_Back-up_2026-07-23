from src.memory.memory import Memory # pyright: ignore[reportMissingImports]
from src.config.config_manager import ConfigManager # type: ignore
from src.system.plugin_manager import PluginManager # type: ignore


class CHITTCore:

    def __init__(self):

        self.memory = Memory()
        self.config = ConfigManager()

        self.plugins = PluginManager()
        self.plugins.load_plugins()

        print("CHITT Core Started")

    def save_memory(self, key, value):
        self.memory.save(key, value)

    def get_memory(self, key):
        return self.memory.load(key)

    def run_plugin(self, plugin_name):

        plugin = self.plugins.get_plugin(plugin_name)

        if plugin:
            return plugin.run()

        return f"Plugin '{plugin_name}' not found."

    def show_plugins(self):
        return self.plugins.list_plugins()

    def assistant_name(self):
        return self.config.get("assistant_name")
    
