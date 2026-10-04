"""
=========================================
CHITT - Long Memory
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os


class LongMemory:

    def __init__(self):

        self.memory = {}

        self.file_path = os.path.join(
            os.path.dirname(__file__),
            "long_memory.json"
        )

        self.load_from_disk()

    # ---------------------------------
    # Save Memory
    # ---------------------------------

    def save(self, key, value):

        self.memory[key] = value

        self.save_to_disk()

    # ---------------------------------
    # Load Memory
    # ---------------------------------

    def load(self, key):

        return self.memory.get(key)

    # ---------------------------------
    # Update Memory
    # ---------------------------------

    def update(self, key, value):

        self.memory[key] = value

        self.save_to_disk()

    # ---------------------------------
    # Delete Memory
    # ---------------------------------

    def delete(self, key):

        if key in self.memory:

            del self.memory[key]

            self.save_to_disk()

            return True

        return False

    # ---------------------------------
    # Check Memory
    # ---------------------------------

    def exists(self, key):

        return key in self.memory

    # ---------------------------------
    # Get All Memory
    # ---------------------------------

    def get_all(self):

        return self.memory

    # ---------------------------------
    # Count Memory
    # ---------------------------------

    def count(self):

        return len(self.memory)

    # ---------------------------------
    # Clear Memory
    # ---------------------------------

    def clear(self):

        self.memory.clear()

        self.save_to_disk()

    # ---------------------------------
    # Save To Disk
    # ---------------------------------

    def save_to_disk(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.memory,
                file,
                indent=4
            )

    # ---------------------------------
    # Load From Disk
    # ---------------------------------

    def load_from_disk(self):

        if not os.path.exists(self.file_path):

            self.memory = {}

            return

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.memory = json.load(file)

        except Exception:

            self.memory = {}

    # ---------------------------------
    # Show Memory
    # ---------------------------------

    def show(self):

        print("\n===== LONG MEMORY =====\n")

        if not self.memory:

            print("Memory Empty.")

            return

        for key, value in self.memory.items():

            print(f"{key} : {value}")


if __name__ == "__main__":

    memory = LongMemory()

    memory.save("name", "AVISHKAR")

    memory.save("assistant", "CHITT")

    memory.show()

    print("\nCount :", memory.count())
    
