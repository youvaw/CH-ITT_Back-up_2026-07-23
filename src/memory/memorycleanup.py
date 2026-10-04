"""
=========================================
CHITT - Memory Cleanup
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from memory.short_memory import ShortMemory
from memory.long_memory import LongMemory
from memory.session_memory import SessionMemory
from memory.user_memory import UserMemory


class MemoryCleanup:

    def __init__(self):

        self.short_memory = ShortMemory()

        self.long_memory = LongMemory()

        self.session_memory = SessionMemory()

        self.user_memory = UserMemory()

    # ---------------------------------
    # Clear Short Memory
    # ---------------------------------

    def clear_short(self):

        self.short_memory.clear()

        return True

    # ---------------------------------
    # Clear Session Memory
    # ---------------------------------

    def clear_session(self):

        self.session_memory.clear()

        return True

    # ---------------------------------
    # Clear Long Memory
    # ---------------------------------

    def clear_long(self):

        self.long_memory.clear()

        return True

    # ---------------------------------
    # Clear User Memory
    # ---------------------------------

    def clear_user(self):

        self.user_memory.clear()

        return True

    # ---------------------------------
    # Clear All Memory
    # ---------------------------------

    def clear_all(self):

        self.clear_short()

        self.clear_session()

        self.clear_long()

        self.clear_user()

        return True

    # ---------------------------------
    # Cleanup Temporary Memory
    # ---------------------------------

    def cleanup_temp(self):

        self.clear_short()

        self.clear_session()

        return True

    # ---------------------------------
    # Status
    # ---------------------------------

    def status(self):

        return {

            "short_memory": self.short_memory.count(),

            "session_memory": self.session_memory.count(),

            "long_memory": self.long_memory.count(),

            "user_memory": self.user_memory.count()

        }

    # ---------------------------------
    # Show Status
    # ---------------------------------

    def show(self):

        print("\n===== MEMORY CLEANUP =====\n")

        data = self.status()

        for key, value in data.items():

            print(f"{key} : {value}")


if __name__ == "__main__":

    cleanup = MemoryCleanup()

    cleanup.show()

    # cleanup.cleanup_temp()

    # cleanup.clear_all()
    
