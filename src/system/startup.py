"""
CHITT Startup Manager
"""

from system.config import *
from logger.logger import Logger
from database.manager import DatabaseManager
from core.brain.brain import Brain
from voice.voice_manager import VoiceManager
from plugins.plugin_manager import PluginManager


class Startup:

    def __init__(self):
        self.logger = None
        self.database = None
        self.brain = None
        self.voice = None
        self.plugins = None

    def initialize_logger(self):
        self.logger = Logger()
        self.logger.info("Logger Initialized")

    def initialize_database(self):
        self.database = DatabaseManager()
        if self.logger:
            self.logger.info("Database Connected")

    def initialize_brain(self):
        self.brain = Brain()
        if self.logger:
            self.logger.info("Brain Initialized")

    def initialize_voice(self):
        self.voice = VoiceManager()
        if self.logger:
            self.logger.info("Voice Initialized")

    def initialize_plugins(self):
        self.plugins = PluginManager()
        if self.logger:
            self.logger.info("Plugin Manager Ready")

    def boot(self):
        print("=" * 60)
        print("Starting CHITT AI...")
        print("=" * 60)

        self.initialize_logger()
        self.initialize_database()
        self.initialize_brain()
        self.initialize_voice()
        self.initialize_plugins()

        print("\nCHITT Started Successfully\n")

        if self.logger:
            self.logger.info("System Ready")

    def shutdown(self):
        if self.database:
            self.database.close()

        if self.logger:
            self.logger.info("System Shutdown")

        print("CHITT Shutdown Complete")


# CHITT.py के लिए standalone start function
def start():
    system = Startup()
    system.boot()
    return system


if __name__ == "__main__":
    system = start()
    system.shutdown()
    
