"""
=========================================
CHITT - Conversation Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class ConversationManager:

    def __init__(self):

        self.chat_history = []

        self.last_user_message = ""

        self.last_assistant_message = ""

    # ---------------------------------
    # Add Conversation
    # ---------------------------------

    def add(self, user_message, assistant_message):

        conversation = {

            "user": user_message,

            "assistant": assistant_message

        }

        self.chat_history.append(conversation)

        self.last_user_message = user_message

        self.last_assistant_message = assistant_message

    # ---------------------------------
    # Reply
    # ---------------------------------

    def reply(self, message):

        self.last_user_message = message

        reply = f"You said: {message}"

        self.last_assistant_message = reply

        self.add(message, reply)

        return reply

    # ---------------------------------
    # Get History
    # ---------------------------------

    def history(self):

        return self.chat_history

    # ---------------------------------
    # Last User Message
    # ---------------------------------

    def last_user(self):

        return self.last_user_message

    # ---------------------------------
    # Last Assistant Message
    # ---------------------------------

    def last_assistant(self):

        return self.last_assistant_message

    # ---------------------------------
    # Total Conversations
    # ---------------------------------

    def count(self):

        return len(self.chat_history)

    # ---------------------------------
    # Clear Conversation
    # ---------------------------------

    def clear(self):

        self.chat_history.clear()

        self.last_user_message = ""

        self.last_assistant_message = ""

    # ---------------------------------
    # Show Conversation
    # ---------------------------------

    def show(self):

        print("\n===== Conversation =====\n")

        if not self.chat_history:

            print("No Conversation Found.")

            return

        for index, chat in enumerate(self.chat_history, start=1):

            print(f"{index}. USER      : {chat['user']}")

            print(f"   CHITT     : {chat['assistant']}")

            print()


if __name__ == "__main__":

    conversation = ConversationManager()

    conversation.reply("Hello")

    conversation.reply("Open YouTube")

    conversation.show()
    
