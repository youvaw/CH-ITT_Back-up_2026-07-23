"""
CHITT AI
Brain Engine
"""

from src.core.intent_engine import IntentEngine # type: ignore
from src.core.command_registry import CommandRegistry # type: ignore
from src.ai.conversation_manager import ConversationManager # pyright: ignore[reportMissingImports]


class BrainEngine:

    def __init__(self, api_key):

        self.intent_engine = IntentEngine()

        self.command_registry = CommandRegistry()

        self.ai = ConversationManager(api_key)

    def process(self, command):

        intent = self.intent_engine.detect(command)

        if intent == "chat":

            return self.ai.chat(command)

        result = self.command_registry.execute(intent)

        if result is None:

            return "Sorry, I don't know how to do that."

        return result
    
