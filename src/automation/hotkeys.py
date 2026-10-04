"""
=========================================
CHITT - Hotkey Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import keyboard


class HotkeyManager:

    def __init__(self):

        self.hotkeys = {}

    # ---------------------------------
    # Register Hotkey
    # ---------------------------------

    def register(

        self,

        hotkey,

        callback

    ):

        try:

            keyboard.add_hotkey(

                hotkey,

                callback

            )

            self.hotkeys[hotkey] = callback

            return {

                "success": True,

                "hotkey": hotkey

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Remove Hotkey
    # ---------------------------------

    def unregister(self, hotkey):

        try:

            keyboard.remove_hotkey(hotkey)

            self.hotkeys.pop(

                hotkey,

                None

            )

            return {

                "success": True

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Remove All
    # ---------------------------------

    def clear(self):

        keyboard.unhook_all_hotkeys()

        self.hotkeys.clear()

        return {

            "success": True

        }

    # ---------------------------------
    # List Hotkeys
    # ---------------------------------

    def list(self):

        return list(

            self.hotkeys.keys()

        )

    # ---------------------------------
    # Exists
    # ---------------------------------

    def exists(self, hotkey):

        return hotkey in self.hotkeys

    # ---------------------------------
    # Wait
    # ---------------------------------

    def wait(self):

        keyboard.wait()

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(

        self,

        command,

        *args

    ):

        command = command.lower()

        if command == "register":

            return self.register(*args)

        elif command == "unregister":

            return self.unregister(*args)

        elif command == "clear":

            return self.clear()

        elif command == "list":

            return self.list()

        elif command == "exists":

            return self.exists(*args)

        return {

            "success": False,

            "message": "Unknown command."

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "HotkeyManager",

            "registered": len(

                self.hotkeys

            ),

            "status": "OK"

        }


if __name__ == "__main__":

    manager = HotkeyManager()

    print(manager.health())
    
