"""
=========================================
CHITT - System Plugin
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import platform
import subprocess
import shutil

from plugins.plugin_base import PluginBase


class SystemPlugin(PluginBase):

    def __init__(self):

        super().__init__()

        self.name = "SystemPlugin"
        self.version = "1.0.0"
        self.description = "System Control Plugin"

    # ---------------------------------
    # Startup
    # ---------------------------------

    def start(self):

        print(f"{self.name} Started")

    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def stop(self):

        print(f"{self.name} Stopped")

    # ---------------------------------
    # Shutdown PC
    # ---------------------------------

    def shutdown(self):

        system = platform.system()

        try:

            if system == "Windows":
                os.system("shutdown /s /t 0")

            elif system == "Linux":
                os.system("shutdown now")

            elif system == "Darwin":
                os.system("sudo shutdown -h now")

            return {
                "success": True,
                "message": "Shutdown command executed."
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ---------------------------------
    # Restart PC
    # ---------------------------------

    def restart(self):

        system = platform.system()

        try:

            if system == "Windows":
                os.system("shutdown /r /t 0")

            elif system == "Linux":
                os.system("reboot")

            elif system == "Darwin":
                os.system("sudo reboot")

            return {
                "success": True,
                "message": "Restart command executed."
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ---------------------------------
    # Open Folder
    # ---------------------------------

    def open_folder(self, path):

        try:

            if platform.system() == "Windows":

                os.startfile(path)

            elif platform.system() == "Linux":

                subprocess.Popen(["xdg-open", path])

            else:

                subprocess.Popen(["open", path])

            return {
                "success": True,
                "path": path
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ---------------------------------
    # Launch Application
    # ---------------------------------

    def launch(self, app):

        try:

            subprocess.Popen(app)

            return {
                "success": True,
                "application": app
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ---------------------------------
    # Disk Usage
    # ---------------------------------

    def disk_usage(self):

        usage = shutil.disk_usage("/")

        return {

            "total": usage.total,

            "used": usage.used,

            "free": usage.free

        }

    # ---------------------------------
    # System Info
    # ---------------------------------

    def system_info(self):

        return {

            "os": platform.system(),

            "release": platform.release(),

            "version": platform.version(),

            "machine": platform.machine(),

            "processor": platform.processor()

        }

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, command, value=None):

        command = command.lower()

        if command == "shutdown":

            return self.shutdown()

        elif command == "restart":

            return self.restart()

        elif command == "open_folder":

            return self.open_folder(value)

        elif command == "launch":

            return self.launch(value)

        elif command == "system_info":

            return self.system_info()

        elif command == "disk":

            return self.disk_usage()

        return {

            "success": False,

            "message": "Unknown command."

        }

    # ---------------------------------
    # Settings
    # ---------------------------------

    def settings(self):

        return {

            "allow_shutdown": False,

            "allow_restart": False

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "plugin": self.name,

            "enabled": self.enabled,

            "status": "OK"

        }


if __name__ == "__main__":

    plugin = SystemPlugin()

    plugin.start()

    print(plugin.system_info())

    print(plugin.disk_usage())

    plugin.stop()
    
