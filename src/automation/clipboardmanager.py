"""
=========================================
CHITT - Clipboard Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import pyperclip
from collections import deque


class ClipboardManager:

    def __init__(self):

        self.history = deque(maxlen=50)

    # ---------------------------------
    # Copy
    # ---------------------------------

    def copy(self, text):

        pyperclip.copy(text)

        self.history.append(text)

        return {

            "success": True,

            "text": text

        }

    # ---------------------------------
    # Paste
    # ---------------------------------

    def paste(self):

        return pyperclip.paste()

    # ---------------------------------
    # Read Clipboard
    # ---------------------------------

    def read(self):

        return {

            "text": pyperclip.paste()

        }

    # ---------------------------------
    # Clear Clipboard
    # ---------------------------------

    def clear(self):

        pyperclip.copy("")

        return {

            "success": True

        }

    # ---------------------------------
    # Clipboard History
    # ---------------------------------

    def get_history(self):

        return list(self.history)

    # ---------------------------------
    # Last Copied Item
    # ---------------------------------

    def last(self):

        if self.history:

            return self.history[-1]

        return None

    # ---------------------------------
    # Restore History Item
    # ---------------------------------

    def restore(self, index):

        try:

            item = self.history[index]

            pyperclip.copy(item)

            return {

                "success": True,

                "text": item

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, command, value=None):

        command = command.lower()

        if command == "copy":

            return self.copy(value)

        elif command == "paste":

            return self.paste()

        elif command == "read":

            return self.read()

        elif command == "clear":

            return self.clear()

        elif command == "history":

            return self.get_history()

        elif command == "last":

            return self.last()

        elif command == "restore":

            return self.restore(value)

        return {

            "success": False,

            "message": "Unknown command."

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "ClipboardManager",

            "history": len(self.history),

            "status": "OK"

        }


if __name__ == "__main__":

    clipboard = ClipboardManager()

    clipboard.copy("Hello CHITT")

    print(clipboard.read())

    print(clipboard.get_history())

    print(clipboard.health())
    
