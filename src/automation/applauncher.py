"""
=========================================
CHITT - App Launcher
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import shutil
import subprocess
import platform


class AppLauncher:

    def __init__(self):

        self.os_name = platform.system()

        self.custom_apps = {}

    # ---------------------------------
    # Register App
    # ---------------------------------

    def register(self, name, path):

        self.custom_apps[name.lower()] = path

    # ---------------------------------
    # Launch Application
    # ---------------------------------

    def launch(self, app):

        app = app.lower()

        try:

            if app in self.custom_apps:

                path = self.custom_apps[app]

                return self.launch_path(path)

            command = shutil.which(app)

            if command:

                subprocess.Popen([command])

                return {

                    "success": True,

                    "application": app

                }

            return {

                "success": False,

                "message": "Application not found."

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Launch Path
    # ---------------------------------

    def launch_path(self, path):

        try:

            if self.os_name == "Windows":

                os.startfile(path)

            elif self.os_name == "Linux":

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
    # Close Process
    # ---------------------------------

    def close(self, process):

        try:

            if self.os_name == "Windows":

                os.system(

                    f"taskkill /F /IM {process}"

                )

            else:

                os.system(

                    f"pkill {process}"

                )

            return {

                "success": True

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Installed
    # ---------------------------------

    def installed(self, app):

        return shutil.which(app) is not None

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, command, value=None):

        command = command.lower()

        if command == "launch":

            return self.launch(value)

        elif command == "close":

            return self.close(value)

        elif command == "installed":

            return {

                "installed":

                self.installed(value)

            }

        return {

            "success": False,

            "message": "Unknown command."

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "AppLauncher",

            "status": "OK",

            "os": self.os_name

        }


if __name__ == "__main__":

    launcher = AppLauncher()

    print(

        launcher.health()

    )

    print(

        launcher.execute(

            "installed",

            "python"

        )

    )
import os
import subprocess
import webbrowser

class AppLauncher:
    def open_app_or_website(self, command: str) -> str:
        """युझरच्या इनपुटनुसार ॲप्स किंवा वेबसाईट उघडणे"""
        cmd = command.lower().strip()

        # ब्राऊझर / वेबसाईट
        if "youtube" in cmd:
            webbrowser.open("https://www.youtube.com")
            return "YouTube उघडत आहे..."
        elif "google" in cmd:
            webbrowser.open("https://www.google.com")
            return "Google उघडत आहे..."

        # सिस्टम ॲप्लिकेशन्स
        elif "notepad" in cmd or "नोटपॅड" in cmd:
            subprocess.Popen(["notepad.exe"])
            return "Notepad उघडत आहे..."
        elif "calculator" in cmd or "calc" in cmd or "कॅल्क्युलेटर" in cmd:
            subprocess.Popen(["calc.exe"])
            return "Calculator उघडत आहे..."
 
        elif "cmd" in cmd or "command prompt" in cmd:
            subprocess.Popen(["cmd.exe"])
            return "Command Prompt उघडत आहे..."

        return None    
