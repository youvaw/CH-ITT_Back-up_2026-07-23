"""
CHITT AI Manager
"""

from .gemini import GeminiClient


class AIManager:

    def __init__(self, api_key: str):
        self.gemini = GeminiClient(api_key)

    def ask(self, prompt: str):

        return self.gemini.generate(prompt) # pyright: ignore[reportAttributeAccessIssue]
    
