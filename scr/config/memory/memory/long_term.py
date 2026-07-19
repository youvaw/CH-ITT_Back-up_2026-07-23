"""
CHITT AI
Long Term Memory
"""


class LongTermMemory:
    """
    Stores permanent knowledge.
    """

    def __init__(self):
        self.memory = {}

    def save(self, key: str, value):

        self.memory[key] = value

    def load(self, key: str):

        return self.memory.get(key)

    def delete(self, key: str):

        if key in self.memory:
            del self.memory[key]

    def exists(self, key: str):

        return key in self.memory

    def clear(self):

        self.memory.clear()

    def all(self):

        return self.memory
    