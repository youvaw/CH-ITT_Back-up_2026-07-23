"""
=========================================
CHITT - Memory Storage
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os

from .shortmemory import ShortMemory
from .longmemory import LongMemory
from .session_memory import SessionMemory
from .usermemory import UserMemory


class MemoryStorage:

    def __init__(self):

        self.short_memory = ShortMemory()

        self.long_memory = LongMemory()

        self.session_memory = SessionMemory()

        self.user_memory = UserMemory()

        self.storage_file = os.path.join(

            os.path.dirname(__file__),

            "memory_storage.json"

        )

    # ---------------------------------
    # Save All Memory
    # ---------------------------------

    def save(self):

        data = {

            "short_memory": self.short_memory.get_all(),

            "long_memory": self.long_memory.get_all(),

            "session_memory": self.session_memory.get_all(),

            "user_memory": self.user_memory.get_all()

        }

        with open(

            self.storage_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False

            )

        return True

    # ---------------------------------
    # Load All Memory
    # ---------------------------------

    def load(self):

        if not os.path.exists(self.storage_file):

            return False

        with open(

            self.storage_file,

            "r",

            encoding="utf-8"

        ) as file:

            data = json.load(file)

        for key, value in data.get(

            "short_memory",

            {}

        ).items():

            self.short_memory.save(key, value)

        for key, value in data.get(

            "long_memory",

            {}

        ).items():

            self.long_memory.save(key, value)

        for key, value in data.get(

            "session_memory",

            {}

        ).items():

            self.session_memory.save(key, value)

        for key, value in data.get(

            "user_memory",

            {}

        ).items():

            self.user_memory.save(key, value)

        return True

    # ---------------------------------
    # Storage Exists
    # ---------------------------------

    def exists(self):

        return os.path.exists(self.storage_file)

    # ---------------------------------
    # Delete Storage
    # ---------------------------------

    def delete(self):

        if self.exists():

            os.remove(self.storage_file)

            return True

        return False

    # ---------------------------------
    # Storage Path
    # ---------------------------------

    def path(self):

        return self.storage_file

    # ---------------------------------
    # Show Storage Info
    # ---------------------------------

    def show(self):

        print("\n===== MEMORY STORAGE =====\n")

        print("Storage File :",

              self.storage_file)

        print("Exists       :",

              self.exists())


if __name__ == "__main__":

    storage = MemoryStorage()

    storage.save()

    storage.load()

    storage.show()
    
