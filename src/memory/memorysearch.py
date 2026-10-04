"""
=========================================
CHITT - Memory Search
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from memory.shortmemory import ShortMemory
from memory.longmemory import LongMemory
from memory.usermemory import UserMemory


class MemorySearch:

    def __init__(self):

        self.short_memory = ShortMemory()

        self.long_memory = LongMemory()

        self.user_memory = UserMemory()

    # ---------------------------------
    # Search All Memory
    # ---------------------------------

    def search(self, keyword):

        keyword = str(keyword).lower()

        results = {

            "short_memory": {},

            "long_memory": {},

            "user_memory": {}

        }

        # Short Memory

        for key, value in self.short_memory.get_all().items():

            if keyword in str(key).lower() or keyword in str(value).lower():

                results["short_memory"][key] = value

        # Long Memory

        for key, value in self.long_memory.get_all().items():

            if keyword in str(key).lower() or keyword in str(value).lower():

                results["long_memory"][key] = value

        # User Memory

        for key, value in self.user_memory.get_all().items():

            if keyword in str(key).lower() or keyword in str(value).lower():

                results["user_memory"][key] = value

        return results

    # ---------------------------------
    # Search Key
    # ---------------------------------

    def search_key(self, key):

        return self.search(key)

    # ---------------------------------
    # Search Value
    # ---------------------------------

    def search_value(self, value):

        return self.search(value)

    # ---------------------------------
    # Print Results
    # ---------------------------------

    def show(self, keyword):

        results = self.search(keyword)

        print("\n===== SEARCH RESULT =====\n")

        for memory_name, memory_data in results.items():

            print(f"\n{memory_name.upper()}")

            if not memory_data:

                print("No Result")

                continue

            for key, value in memory_data.items():

                print(f"{key} : {value}")


if __name__ == "__main__":

    search = MemorySearch()

    search.show("name")
    
