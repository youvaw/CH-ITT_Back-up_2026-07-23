import os
import importlib.util


class PluginLoader:

    def __init__(self):
        self.plugins = {}

    def load_plugins(self, plugin_folder):

        if not os.path.exists(plugin_folder):
            return {}

        for file in os.listdir(plugin_folder):

            if not file.endswith(".py"):
                continue

            if file.startswith("__"):
                continue

            plugin_name = file[:-3]

            path = os.path.join(plugin_folder, file)

            spec = importlib.util.spec_from_file_location(
                plugin_name,
                path
            )

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            self.plugins[plugin_name] = module

        return self.plugins

    def get_plugins(self):
        return self.plugins
    
