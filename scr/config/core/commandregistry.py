"""
CHITT AI
Command Registry
"""

from src.skills.basic_commands import BasicCommands # type: ignore


class CommandRegistry:

    def __init__(self):

        self.basic = BasicCommands()

        self.commands = {

            "open_google": self.basic.open_google,

            "open_youtube": self.basic.open_youtube,

            "open_github": self.basic.open_github,

            "open_notepad": self.basic.open_notepad,

            "open_calculator": self.basic.open_calculator,

            "open_paint": self.basic.open_paint,

            "open_cmd": self.basic.open_cmd,

            "open_explorer": self.basic.open_explorer,

            "open_downloads": self.basic.open_downloads,

            "open_documents": self.basic.open_documents,

            "time": self.basic.get_time,

            "date": self.basic.get_date,

            "battery": self.basic.battery
        }

    def execute(self, intent):

        if intent not in self.commands:

            return None

        return self.commands[intent]()
    