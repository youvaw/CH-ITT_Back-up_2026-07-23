"""
=========================================
CHITT - Context Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class ContextManager:

    def __init__(self):

        self.context = {}

        self.history = []

    # ---------------------------------
    # Save Context
    # ---------------------------------

    def save(self, key, value):

        self.context[key] = value

    # ---------------------------------
    # Load Context
    # ---------------------------------

    def load(self, key):

        return self.context.get(key)

    # ---------------------------------
    # Remove Context
    # ---------------------------------

    def remove(self, key):

        if key in self.context:

            del self.context[key]

    # ---------------------------------
    # Clear Context
    # ---------------------------------

    def clear(self):

        self.context.clear()

    # ---------------------------------
    # Add Conversation
    # ---------------------------------

    def add_history(self, user_message, assistant_reply):

        self.history.append({

            "user": user_message,

            "assistant": assistant_reply

        })

    # ---------------------------------
    # Get Conversation History
    # ---------------------------------

    def get_history(self):

        return self.history

    # ---------------------------------
    # Last Conversation
    # ---------------------------------

    def last(self):

        if self.history:

            return self.history[-1]

        return None

    # ---------------------------------
    # Total History
    # ---------------------------------

    def count(self):

        return len(self.history)

    # ---------------------------------
    # Clear History
    # ---------------------------------

    def clear_history(self):

        self.history.clear()

    # ---------------------------------
    # Show Context
    # ---------------------------------

    def show(self):

        print("===== Context =====")

        for key, value in self.context.items():

            print(f"{key} : {value}")

        print("\n===== History =====")

        for chat in self.history:

            print(chat)


if __name__ == "__main__":

    context = ContextManager()

    context.save("user_name", "AVISHKAR")

    context.save("language", "English")

    context.add_history(

        "Hello CHITT",

        "Hello AVISHKAR"

    )

    context.show()
    
