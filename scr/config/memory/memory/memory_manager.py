"""
CHITT AI
Memory Manager
"""

from short_term import ShortTermMemory
from long_term import LongTermMemory


class MemoryManager:

    def __init__(self):

        self.short = ShortTermMemory()
        self.long = LongTermMemory()

    def remember(self, key, value):

        self.short.save(key, value) # pyright: ignore[reportAttributeAccessIssue]
        self.long.save(key, value)

    def recall(self, key):

        value = self.short.load(key) # pyright: ignore[reportAttributeAccessIssue]

        if value is None:
            value = self.long.load(key)

        return value

    def forget(self, key):

        self.short.delete(key) # pyright: ignore[reportAttributeAccessIssue]
        self.long.delete(key)

    def clear(self):

        self.short.clear()
        self.long.clear()