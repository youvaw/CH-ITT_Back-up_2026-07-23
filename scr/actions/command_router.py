"""
CHITT AI
Command Router
"""

from .app_launcher import AppLauncher
from .browser import Browser


class CommandRouter:

    def __init__(self):

        self.apps = AppLauncher()

        self.browser = Browser()

    def execute(self, command):

        command = command.lower()

        if "notepad" in command:
            self.apps.open_notepad()

        elif "calculator" in command:
            self.apps.open_calculator()

        elif "paint" in command:
            self.apps.open_paint()

        elif "cmd" in command:
            self.apps.open_cmd()

        elif "youtube" in command:
            self.browser.open_youtube()

        elif "google" == command:
            self.browser.open_google()

        else:

            return False

        return True
    