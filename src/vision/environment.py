"""
=========================================
CHITT - Vision Environment
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import cv2
import pytesseract
import numpy as np

from vision.config import *


class Environment:

    def __init__(self):

        self.status = {}

    # ---------------------------------
    # Check OpenCV
    # ---------------------------------

    def check_opencv(self):

        try:

            version = cv2.__version__

            self.status["opencv"] = version

            return True

        except Exception:

            self.status["opencv"] = False

            return False

    # ---------------------------------
    # Check NumPy
    # ---------------------------------

    def check_numpy(self):

        try:

            version = np.__version__

            self.status["numpy"] = version

            return True

        except Exception:

            self.status["numpy"] = False

            return False

    # ---------------------------------
    # Check OCR
    # ---------------------------------

    def check_ocr(self):

        try:

            version = pytesseract.get_tesseract_version()

            self.status["tesseract"] = str(version)

            return True

        except Exception:

            self.status["tesseract"] = False

            return False

    # ---------------------------------
    # Camera Test
    # ---------------------------------

    def check_camera(self):

        camera = cv2.VideoCapture(DEFAULT_CAMERA)

        ok = camera.isOpened()

        camera.release()

        self.status["camera"] = ok

        return ok

    # ---------------------------------
    # Folder Check
    # ---------------------------------

    def check_folders(self):

        folders = REQUIRED_FOLDERS

        result = True

        for folder in folders:

            if not os.path.exists(folder):

                os.makedirs(folder, exist_ok=True)

            if not os.path.exists(folder):

                result = False

        self.status["folders"] = result

        return result

    # ---------------------------------
    # Model Check
    # ---------------------------------

    def check_models(self):

        models = {

            "cfg": os.path.exists(YOLO_CFG),

            "weights": os.path.exists(YOLO_WEIGHTS),

            "classes": os.path.exists(YOLO_CLASSES)

        }

        self.status["models"] = models

        return models

    # ---------------------------------
    # Full Test
    # ---------------------------------

    def run(self):

        self.check_opencv()

        self.check_numpy()

        self.check_ocr()

        self.check_camera()

        self.check_folders()

        self.check_models()

        return self.status

    # ---------------------------------
    # Print Report
    # ---------------------------------

    def report(self):

        print("\n========== CHITT Vision ==========\n")

        for key, value in self.status.items():

            print(f"{key:15} : {value}")

        print("\n==================================\n")


if __name__ == "__main__":

    env = Environment()

    env.run()

    env.report()
    
