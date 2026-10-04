"""
=========================================
CHITT - Voice Commands
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from commands.command_router import CommandRouter


class VoiceCommands:

    def __init__(self):

        self.router = CommandRouter()

    # ---------------------------------
    # Execute Voice Command
    # ---------------------------------

    def execute(self, command):

        if not command:

            return "No command received."

        command = command.strip()

        print(f"Voice Command : {command}")

        return self.router.route(command)

    # ---------------------------------
    # Validate Command
    # ---------------------------------

    def validate(self, command):

        if command is None:

            return False

        if not isinstance(command, str):

            return False

        if command.strip() == "":

            return False

        return True

    # ---------------------------------
    # Process Command
    # ---------------------------------

    def process(self, command):

        if not self.validate(command):

            return "Invalid Command"

        return self.execute(command)

    # ---------------------------------
    # Show Command
    # ---------------------------------

    def show(self, command):

        print("=================================")

        print("VOICE COMMAND")

        print("---------------------------------")

        print(command)

        print("=================================")


if __name__ == "__main__":

    voice = VoiceCommands()

    result = voice.process("Open YouTube")

    print(result)
    