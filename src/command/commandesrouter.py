from commands.web_commands import WebCommands
from commands.app_commands import AppCommands
from commands.system_commands import SystemCommands


class CommandRouter:

    def __init__(self):

        self.web = WebCommands()
        self.app = AppCommands()
        self.system = SystemCommands()

    def execute(self, command):

        command = command.lower()

        if "youtube" in command:
            return self.web.open_youtube()

        elif "google" in command:
            return self.web.open_google()

        elif "github" in command:
            return self.web.open_github()

        elif "notepad" in command:
            return self.app.open_notepad()

        elif "calculator" in command:
            return self.app.open_calculator()

        elif "cmd" in command:
            return self.app.open_cmd()

        elif "shutdown" in command:
            return self.system.shutdown()

        elif "restart" in command:
            return self.system.restart()

        elif "lock" in command:
            return self.system.lock()

        return False
    
