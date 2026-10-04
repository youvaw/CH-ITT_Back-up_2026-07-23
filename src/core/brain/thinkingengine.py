"""
=========================================
CHITT - Thinking Engine
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from brain.intent_classifier import IntentClassifier
from core.brain.decision_engine import DecisionEngine
from brain.response_manager import ResponseManager
from brain.context_manager import ContextManager
from brain.task_manager import TaskManager
from brain.conversation_manager import ConversationManager
from brain.emotion_manager import EmotionManager


class ThinkingEngine:

    def __init__(self):

        self.intent = IntentClassifier()

        self.decision = DecisionEngine()

        self.response = ResponseManager()

        self.context = ContextManager()

        self.task = TaskManager()

        self.conversation = ConversationManager()

        self.emotion = EmotionManager()

    # ---------------------------------
    # Main Thinking Process
    # ---------------------------------

    def process(self, command):

        if not command:

            return "No command received."

        # Detect Emotion
        emotion = self.emotion.detect(command)

        # Detect Intent
        intent = self.intent.detect(command)

        # Make Decision
        decision = self.decision.make(intent)

        # Generate Response
        reply = self.response.generate(decision)

        # Save Conversation
        self.conversation.add(command, reply)

        # Save Context
        self.context.save("last_command", command)

        self.context.save("last_intent", intent)

        self.context.save("last_emotion", emotion)

        return {

            "command": command,

            "emotion": emotion,

            "intent": intent,

            "decision": decision,

            "response": reply

        }

    # ---------------------------------
    # Last Command
    # ---------------------------------

    def last_command(self):

        return self.context.load("last_command")

    # ---------------------------------
    # Last Intent
    # ---------------------------------

    def last_intent(self):

        return self.context.load("last_intent")

    # ---------------------------------
    # Last Emotion
    # ---------------------------------

    def last_emotion(self):

        return self.context.load("last_emotion")

    # ---------------------------------
    # Show Brain Status
    # ---------------------------------

    def status(self):

        print("\n===== CHITT Brain Status =====")

        print("Last Command :", self.last_command())

        print("Last Intent  :", self.last_intent())

        print("Last Emotion :", self.last_emotion())

        print("Conversation :", self.conversation.count())

        print("Tasks        :", self.task.count())

        print("===============================")


if __name__ == "__main__":

    brain = ThinkingEngine()

    result = brain.process("Open YouTube")

    print(result)

    brain.status()
    
