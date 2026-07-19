"""
CHITT AI
Application Launcher
"""

import subprocess


class AppLauncher:

    def open_notepad(self):

        subprocess.Popen("notepad.exe")

    def open_calculator(self):

        subprocess.Popen("calc.exe")

    def open_paint(self):

        subprocess.Popen("mspaint.exe")

    def open_cmd(self):

        subprocess.Popen("cmd.exe")
        