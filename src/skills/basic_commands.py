"""
CHITT AI
Basic Commands Engine
"""

import webbrowser
import subprocess
import os
import datetime
import psutil


class BasicCommands:

    def open_google(self):
        webbrowser.open("https://www.google.com")

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com")

    def open_github(self):
        webbrowser.open("https://github.com")

    def open_notepad(self):
        subprocess.Popen("notepad.exe")

    def open_calculator(self):
        subprocess.Popen("calc.exe")

    def open_paint(self):
        subprocess.Popen("mspaint.exe")

    def open_cmd(self):
        subprocess.Popen("cmd.exe")

    def open_explorer(self):
        subprocess.Popen("explorer.exe")

    def open_downloads(self):
        path = os.path.join(os.path.expanduser("~"), "Downloads")
        os.startfile(path)

    def open_documents(self):
        path = os.path.join(os.path.expanduser("~"), "Documents")
        os.startfile(path)

    def get_time(self):
        return datetime.datetime.now().strftime("%I:%M %p")

    def get_date(self):
        return datetime.datetime.now().strftime("%d-%m-%Y")

    def battery(self):

        battery = psutil.sensors_battery()

        if battery is None:
            return "Battery information unavailable."

        return f"Battery is {battery.percent}%"
    
