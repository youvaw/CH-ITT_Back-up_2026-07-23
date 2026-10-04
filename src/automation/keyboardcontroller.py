"""
=========================================
CHITT - Keyboard Controller
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import keyboard
import time


class KeyboardController:

    def __init__(self):

        self.delay = 0.05

    # ---------------------------------
    # Type Text
    # ---------------------------------

    def write(self, text):

        keyboard.write(

            text,

            delay=self.delay

        )

        return True

    # ---------------------------------
    # Press Key
    # ---------------------------------

    def press(self, key):

        keyboard.press_and_release(key)

        return True

    # ---------------------------------
    # Hold Key
    # ---------------------------------

    def hold(self, key):

        keyboard.press(key)

    # ---------------------------------
    # Release Key
    # ---------------------------------

    def release(self, key):

        keyboard.release(key)

    # ---------------------------------
    # Hotkey
    # ---------------------------------

    def shortcut(self, *keys):

        keyboard.press_and_release(

            "+".join(keys)

        )

        return True

    # ---------------------------------
    # Enter
    # ---------------------------------

    def enter(self):

        return self.press("enter")

    # ---------------------------------
    # Backspace
    # ---------------------------------

    def backspace(self):

        return self.press("backspace")

    # ---------------------------------
    # Tab
    # ---------------------------------

    def tab(self):

        return self.press("tab")

    # ---------------------------------
    # Escape
    # ---------------------------------

    def escape(self):

        return self.press("esc")

    # ---------------------------------
    # Copy
    # ---------------------------------

    def copy(self):

        return self.shortcut(

            "ctrl",

            "c"

        )

    # ---------------------------------
    # Paste
    # ---------------------------------

    def paste(self):

        return self.shortcut(

            "ctrl",

            "v"

        )

    # ---------------------------------
    # Cut
    # ---------------------------------

    def cut(self):

        return self.shortcut(

            "ctrl",

            "x"

        )

    # ---------------------------------
    # Undo
    # ---------------------------------

    def undo(self):

        return self.shortcut(

            "ctrl",

            "z"

        )

    # ---------------------------------
    # Save
    # ---------------------------------

    def save(self):

        return self.shortcut(

            "ctrl",

            "s"

        )

    # ---------------------------------
    # Select All
    # ---------------------------------

    def select_all(self):

        return self.shortcut(

            "ctrl",

            "a"

        )

    # ---------------------------------
    # Delay
    # ---------------------------------

    def wait(self, seconds):

        time.sleep(seconds)

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "KeyboardController",

            "status": "OK",

            "delay": self.delay

        }


if __name__ == "__main__":

    kb = KeyboardController()

    print(kb.health())
    
