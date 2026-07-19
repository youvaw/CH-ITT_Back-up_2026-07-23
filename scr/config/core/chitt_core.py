"""
CHITT Core
Main AI Controller
"""

from src.ai.conversation_manager import ConversationManager # type: ignore
from src.voice.voice_manager import VoiceManager # type: ignore


class CHITTCore:

    def __init__(self, api_key):

        self.voice = VoiceManager()

        self.conversation = ConversationManager(api_key)

    def start(self):

        self.voice.speak("Hello, I am CHITT AI.")

        while True:

            user = self.voice.listen()

            if not user:
                continue

            print("You :", user)

            if user.lower() in ["exit", "quit", "bye"]:

                self.voice.speak("Goodbye.")

                break

            reply = self.conversation.chat(user)

            self.voice.speak(reply)
