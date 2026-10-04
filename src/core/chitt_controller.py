"""
CHITT Main Controller
"""

from src.voice.voice_manager import VoiceManager # type: ignore
from src.ai.conversation_manager import ConversationManager # type: ignore
from src.vision.actions.command_router import CommandRouter # pyright: ignore[reportMissingImports]


class CHITTController:

    def __init__(self, api_key):

        self.voice = VoiceManager()

        self.ai = ConversationManager(api_key)

        self.router = CommandRouter()

    def run(self):

        self.voice.speak("Hello. I am CHITT AI.")

        while True:

            command = self.voice.listen()

            if command is None:
                continue

            print(f"You : {command}")

            if command.lower() in ["exit", "quit", "bye"]:

                self.voice.speak("Goodbye.")

                break

            executed = self.router.execute(command)

            if executed:

                self.voice.speak("Done.")

                continue

            answer = self.ai.chat(command)

            self.voice.speak(answer)

