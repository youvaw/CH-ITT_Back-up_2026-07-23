"""
=========================================
CHITT - Mouse Controller
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import pyautogui
import time


class MouseController:

    def __init__(self):

        pyautogui.FAILSAFE = True

        self.duration = 0.25

    # ---------------------------------
    # Move Mouse
    # ---------------------------------

    def move(self, x, y):

        pyautogui.moveTo(

            x,

            y,

            duration=self.duration

        )

        return True

    # ---------------------------------
    # Relative Move
    # ---------------------------------

    def move_relative(

        self,

        dx,

        dy

    ):

        pyautogui.moveRel(

            dx,

            dy,

            duration=self.duration

        )

        return True

    # ---------------------------------
    # Left Click
    # ---------------------------------

    def click(

        self,

        x=None,

        y=None

    ):

        pyautogui.click(

            x=x,

            y=y

        )

        return True

    # ---------------------------------
    # Double Click
    # ---------------------------------

    def double_click(

        self,

        x=None,

        y=None

    ):

        pyautogui.doubleClick(

            x=x,

            y=y

        )

        return True

    # ---------------------------------
    # Right Click
    # ---------------------------------

    def right_click(

        self,

        x=None,

        y=None

    ):

        pyautogui.rightClick(

            x=x,

            y=y

        )

        return True

    # ---------------------------------
    # Middle Click
    # ---------------------------------

    def middle_click(

        self,

        x=None,

        y=None

    ):

        pyautogui.middleClick(

            x=x,

            y=y

        )

        return True

    # ---------------------------------
    # Drag
    # ---------------------------------

    def drag(

        self,

        x,

        y

    ):

        pyautogui.dragTo(

            x,

            y,

            duration=self.duration,

            button="left"

        )

        return True

    # ---------------------------------
    # Scroll
    # ---------------------------------

    def scroll(self, amount):

        pyautogui.scroll(amount)

        return True

    # ---------------------------------
    # Mouse Position
    # ---------------------------------

    def position(self):

        x, y = pyautogui.position()

        return {

            "x": x,

            "y": y

        }

    # ---------------------------------
    # Wait
    # ---------------------------------

    def wait(self, seconds):

        time.sleep(seconds)

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "MouseController",

            "status": "OK",

            "duration": self.duration

        }


if __name__ == "__main__":

    mouse = MouseController()

    print(mouse.position())

    print(mouse.health())
    
