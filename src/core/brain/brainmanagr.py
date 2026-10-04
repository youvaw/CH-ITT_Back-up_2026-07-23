"""
=========================================
CHITT - Brain Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from src.brain.intentclassifier import IntentClassifier
from core.brain.decisionengine import DecisionEngine
from src.brain.responsemanager import ResponseManager
from core.brain.contextmanager import ContextManager
from core.brain.taskmanager import TaskManager
from src.brain.conversationmanager import ConversationManager
from src.brain.emotionmanager import EmotionManager
from core.brain.thinkingengine import ThinkingEngine


class BrainManager:

    def __init__(self):

        self.intent = IntentClassifier()

        self.decision = DecisionEngine()

        self.response = ResponseManager()

        self.context = ContextManager()

        self.task = TaskManager()

        self.conversation = ConversationManager()

        self.emotion = EmotionManager()

        self.thinking = ThinkingEngine()

    # --------------------------
    # Main Brain Process
    # --------------------------

    def process(self, command):

        intent = self.intent.detect(command)

        decision = self.decision.make(intent)

        response = self.response.generate(decision)

        return response

    # --------------------------
    # Context
    # --------------------------

    def remember(self, key, value):

        self.context.save(key, value)

    def recall(self, key):

        return self.context.load(key)

    # --------------------------
    # Tasks
    # --------------------------

    def add_task(self, task):

        self.task.add(task)

    def get_tasks(self):

        return self.task.list()

    # --------------------------
    # Thinking
    # --------------------------

    def think(self, command):

        return self.thinking.process(command)

    # --------------------------
    # Emotion
    # --------------------------

    def emotion_state(self):

        return self.emotion.current()

    # --------------------------
    # Conversation
    # --------------------------

    def chat(self, message):

        return self.conversation.reply(message)


if __name__ == "__main__":

    brain = BrainManager()

    result = brain.process("Open YouTube")

    print(result)
    
