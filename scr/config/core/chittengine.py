"""
CHITT AI
Main Engine
"""

from src.core.brain_engine import BrainEngine # pyright: ignore[reportMissingImports]
from src.config.config_manager import ConfigManager # pyright: ignore[reportMissingImports]


class CHITTEngine:

    def __init__(self):

        self.config = ConfigManager()

        api_key = self.config.get("gemini_api_key")

        self.brain = BrainEngine(api_key)

    def execute(self, command):

        command = command.strip()

        if command == "":
            return "Please say something."

        return self.brain.process(command)
    