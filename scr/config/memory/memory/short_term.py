"""
CHITT AI
Short Term Memory
"""

from typing import Any


class ShortTermMemory:

    def __init__(self):
        self.memory = {}

    def add(self, key: str, value: Any):
        self.memory[key] = value

    def get(self, key: str):
        return self.memory.get(key)

    def remove(self, key: str):
        if key in self.memory:
            del self.memory[key]

    def clear(self):
        self.memory.clear()

    def size(self):
        return len(self.memory)

    def all(self):
        return self.memory
    