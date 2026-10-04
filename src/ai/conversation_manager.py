"""
CHITT Conversation Manager
"""

from .ai_manager import AIManager
from .prompt_builder import PromptBuilder


class ConversationManager:

    def __init__(self, api_key):

        self.ai = AIManager(api_key)
        self.prompt = PromptBuilder()

    def chat(self, user_message):

        prompt = self.prompt.build(user_message)

        answer = self.ai.ask(prompt)

        return answer
    
