"""
CHITT Plugin Installer
"""

from pathlib import Path
import shutil


class PluginInstaller:

    def __init__(self):

        self.plugin_folder = Path("plugins")

        self.plugin_folder.mkdir(

            parents=True,

            exist_ok=True

        )

    # ==========================================
    # Install Plugin
    # ==========================================

    def install(self, source):

        source = Path(source)

        destination = self.plugin_folder / source.name

        shutil.copy(source, destination)

        return destination

    # ==========================================
    # Remove Plugin
    # ==========================================

    def uninstall(self, plugin_name):

        plugin = self.plugin_folder / plugin_name

        if plugin.exists():

            plugin.unlink()

            return True

        return False

    # ==========================================
    # Installed Plugins
    # ==========================================

    def installed(self):

        return [

            file.name

            for file in self.plugin_folder.glob("*.py")

        ]
    
