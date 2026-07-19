"""
CHITT AI
Application Manager
"""

import subprocess
import psutil


class AppManager:

    def open_app(self, app_name):

        apps = {

            "notepad": "notepad.exe",

            "calculator": "calc.exe",

            "paint": "mspaint.exe",

            "cmd": "cmd.exe",

            "explorer": "explorer.exe",

            "settings": "start ms-settings:",

            "store": "start ms-windows-store:"
        }

        if app_name not in apps:

            return False

        command = apps[app_name]

        if command.startswith("start"):

            subprocess.Popen(command, shell=True)

        else:

            subprocess.Popen(command)

        return True

    def close_app(self, process_name):

        process_name = process_name.lower()

        for process in psutil.process_iter(["name"]):

            try:

                if process.info["name"] and process.info["name"].lower() == process_name:

                    process.kill()

                    return True

            except Exception:

                pass

        return False
    