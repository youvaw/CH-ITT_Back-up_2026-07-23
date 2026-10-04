"""
=========================================
CHITT - Window Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import pygetwindow as gw


class WindowManager:

    def __init__(self):

        self.windows = []

    # ---------------------------------
    # Refresh Window List
    # ---------------------------------

    def refresh(self):

        self.windows = gw.getAllTitles()

        return self.windows

    # ---------------------------------
    # List Windows
    # ---------------------------------

    def list(self):

        return [

            title

            for title in gw.getAllTitles()

            if title.strip()

        ]

    # ---------------------------------
    # Find Window
    # ---------------------------------

    def find(self, title):

        windows = gw.getWindowsWithTitle(title)

        return windows

    # ---------------------------------
    # Activate Window
    # ---------------------------------

    def activate(self, title):

        try:

            window = gw.getWindowsWithTitle(title)[0]

            window.activate()

            return True

        except Exception:

            return False

    # ---------------------------------
    # Minimize
    # ---------------------------------

    def minimize(self, title):

        try:

            window = gw.getWindowsWithTitle(title)[0]

            window.minimize()

            return True

        except Exception:

            return False

    # ---------------------------------
    # Maximize
    # ---------------------------------

    def maximize(self, title):

        try:

            window = gw.getWindowsWithTitle(title)[0]

            window.maximize()

            return True

        except Exception:

            return False

    # ---------------------------------
    # Restore
    # ---------------------------------

    def restore(self, title):

        try:

            window = gw.getWindowsWithTitle(title)[0]

            window.restore()

            return True

        except Exception:

            return False

    # ---------------------------------
    # Close
    # ---------------------------------

    def close(self, title):

        try:

            window = gw.getWindowsWithTitle(title)[0]

            window.close()

            return True

        except Exception:

            return False

    # ---------------------------------
    # Move
    # ---------------------------------

    def move(

        self,

        title,

        x,

        y

    ):

        try:

            window = gw.getWindowsWithTitle(title)[0]

            window.moveTo(x, y)

            return True

        except Exception:

            return False

    # ---------------------------------
    # Resize
    # ---------------------------------

    def resize(

        self,

        title,

        width,

        height

    ):

        try:

            window = gw.getWindowsWithTitle(title)[0]

            window.resizeTo(

                width,

                height

            )

            return True

        except Exception:

            return False

    # ---------------------------------
    # Window Information
    # ---------------------------------

    def info(self, title):

        try:

            window = gw.getWindowsWithTitle(title)[0]

            return {

                "title": window.title,

                "left": window.left,

                "top": window.top,

                "width": window.width,

                "height": window.height,

                "visible": not window.isMinimized

            }

        except Exception:

            return None

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "WindowManager",

            "windows": len(self.list()),

            "status": "OK"

        }


if __name__ == "__main__":

    manager = WindowManager()

    print(manager.health())

    print(manager.list())
