"""
=========================================
CHITT - Image Capture
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import cv2
from datetime import datetime

from vision.camera import Camera


class ImageCapture:

    def __init__(self):

        self.camera = Camera()

        self.save_directory = "captures"

        os.makedirs(self.save_directory, exist_ok=True)

    # ---------------------------------
    # Capture Image
    # ---------------------------------

    def capture(self):

        if not self.camera.start():

            return None

        frame = self.camera.read()

        self.camera.stop()

        if frame is None:

            return None

        filename = self.generate_filename()

        filepath = os.path.join(

            self.save_directory,

            filename

        )

        cv2.imwrite(filepath, frame)

        print(f"Image Saved : {filepath}")

        return filepath

    # ---------------------------------
    # Generate Filename
    # ---------------------------------

    def generate_filename(self):

        timestamp = datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )

        return f"capture_{timestamp}.jpg"

    # ---------------------------------
    # Capture Without Saving
    # ---------------------------------

    def capture_frame(self):

        if not self.camera.start():

            return None

        frame = self.camera.read()

        self.camera.stop()

        return frame

    # ---------------------------------
    # Change Save Folder
    # ---------------------------------

    def set_directory(self, directory):

        self.save_directory = directory

        os.makedirs(

            self.save_directory,

            exist_ok=True

        )

    # ---------------------------------
    # Get Save Folder
    # ---------------------------------

    def get_directory(self):

        return self.save_directory

    # ---------------------------------
    # Last Image
    # ---------------------------------

    def latest_image(self):

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

        return max(files, key=os.path.getctime)


if __name__ == "__main__":

    capture = ImageCapture()

    image = capture.capture()

    print(image)
    
