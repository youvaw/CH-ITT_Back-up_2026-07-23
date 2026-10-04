"""
=========================================
CHITT - Screenshot Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
from datetime import datetime

import cv2
import numpy as np
import pyautogui


class Screenshot:

    def __init__(self):

        self.save_directory = "screenshots"

        os.makedirs(

            self.save_directory,

            exist_ok=True

        )

    # ---------------------------------
    # Capture Full Screen
    # ---------------------------------

    def capture(self):

        image = pyautogui.screenshot()

        frame = cv2.cvtColor(

            np.array(image),

            cv2.COLOR_RGB2BGR

        )

        return frame

    # ---------------------------------
    # Capture Region
    # ---------------------------------

    def capture_region(

        self,

        left,

        top,

        width,

        height

    ):

        image = pyautogui.screenshot(

            region=(

                left,

                top,

                width,

                height

            )

        )

        frame = cv2.cvtColor(

            np.array(image),

            cv2.COLOR_RGB2BGR

        )

        return frame

    # ---------------------------------
    # Save Screenshot
    # ---------------------------------

    def save(self, frame):

        filename = self.filename()

        path = os.path.join(

            self.save_directory,

            filename

        )

        cv2.imwrite(path, frame)

        print(f"Saved : {path}")

        return path

    # ---------------------------------
    # Capture + Save
    # ---------------------------------

    def capture_save(self):

        frame = self.capture()

        return self.save(frame)

    # ---------------------------------
    # Generate Filename
    # ---------------------------------

    def filename(self):

        stamp = datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )

        return f"screenshot_{stamp}.png"

    # ---------------------------------
    # Show Screenshot
    # ---------------------------------

    def show(self, frame):

        cv2.imshow(

            "CHITT Screenshot",

            frame

        )

        cv2.waitKey(0)

        cv2.destroyAllWindows()

    # ---------------------------------
    # Latest Screenshot
    # ---------------------------------

    def latest(self):

        files = [

            os.path.join(

                self.save_directory,

                file

            )

            for file in os.listdir(

                self.save_directory

            )

        ]

        if not files:

            return None

        return max(

            files,

            key=os.path.getctime

        )

    # ---------------------------------
    # Delete Screenshot
    # ---------------------------------

    def delete(self, path):

        if os.path.exists(path):

            os.remove(path)

            return True

        return False

    # ---------------------------------
    # Screenshot Information
    # ---------------------------------

    def info(self):

        return {

            "directory": self.save_directory,

            "latest": self.latest()

        }


if __name__ == "__main__":

    screen = Screenshot()

    image = screen.capture()

    screen.show(image)

    screen.save(image)

    print(screen.info())
    
