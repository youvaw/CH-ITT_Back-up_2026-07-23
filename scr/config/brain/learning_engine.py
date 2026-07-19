"""
CHITT AI
Learning Engine
"""


class LearningEngine:
    """
    Learns from conversations and stores knowledge.
    """

    def __init__(self):
        self.knowledge = {}

    def learn(self, key: str, value: str):

        self.knowledge[key] = value

    def recall(self, key: str):

        return self.knowledge.get(key, None)

    def forget(self, key: str):

        if key in self.knowledge:
            del self.knowledge[key]

    def clear(self):

        self.knowledge.clear()
        