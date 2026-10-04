"""
=========================================
CHITT - Short Memory
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class ShortMemory:

    def __init__(self):

        self.memory = {}

    # ---------------------------------
    # Save Memory
    # ---------------------------------

    def save(self, key, value):

        self.memory[key] = value

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

    # ---------------------------------
    # Delete Memory
    # ---------------------------------

    def delete(self, key):

        if key in self.memory:

            del self.memory[key]

            return True

        return False

    # ---------------------------------
    # Check Key
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

    # ---------------------------------
    # Show Memory
    # ---------------------------------

    def show(self):

        print("\n===== SHORT MEMORY =====\n")

        if not self.memory:

            print("Memory Empty.")

            return

        for key, value in self.memory.items():

            print(f"{key} : {value}")


if __name__ == "__main__":

    memory = ShortMemory()

    memory.save("name", "AVISHKAR")

    memory.save("city", "Mumbai")

    memory.show()

    print("\nCount :", memory.count())

    print("\nName :", memory.load("name"))
    
