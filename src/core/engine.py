"""
=========================================
CHITT - Core Engine
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from brain.brain_manager import BrainManager
from memory.memorymanager import MemoryManager
from voice.voice_manager import VoiceManager
from commands.command_router import CommandRouter
from settings.settings_manager import SettingsManager


class Engine:

    def __init__(self):

        self.brain = BrainManager()

        self.memory = MemoryManager()

        self.voice = VoiceManager()

        self.commands = CommandRouter()

        self.settings = SettingsManager()

        self.running = False

    # ---------------------------------
    # Initialize
    # ---------------------------------

    def initialize(self):

        print("Initializing CHITT Core Engine...")

        return True

    # ---------------------------------
    # Start
    # ---------------------------------

    def start(self):

        self.initialize()

        self.running = True

        self.voice.start()

        print("CHITT Engine Started")

    # ---------------------------------
    # Stop
    # ---------------------------------

    def stop(self):

        self.running = False

        self.voice.stop()

        print("CHITT Engine Stopped")

    # ---------------------------------
    # Listen
    # ---------------------------------

    def listen(self):

        return self.voice.listen()

    # ---------------------------------
    # Think
    # ---------------------------------

    def think(self, command):

        return self.brain.process(command)

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, command):

        return self.commands.route(command)

    # ---------------------------------
    # Speak
    # ---------------------------------

    def speak(self, text):

        self.voice.speak(text)

    # ---------------------------------
    # Main Loop
    # ---------------------------------

    def run(self):

        self.start()

        while self.running:

            command = self.listen()

            if not command:

                continue

            self.memory.save(command)

            response = self.think(command)

            self.execute(command)

            self.speak(response)


if __name__ == "__main__":

    engine = Engine()

    engine.run()
    
