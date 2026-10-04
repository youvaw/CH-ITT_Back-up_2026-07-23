"""
=========================================
CHITT - Vision Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os


class VisionSettings:

    def __init__(self):

        self.file = "vision/config.json"

        self.settings = {

            "camera_id": 0,

            "camera_width": 1280,

            "camera_height": 720,

            "camera_fps": 30,

            "save_images": True,

            "save_screenshots": True,

            "image_format": "png",

            "ocr_language": "eng",

            "ocr_enabled": True,

            "object_detection": True,

            "face_recognition": True,

            "confidence": 0.50,

            "show_preview": True,

            "auto_enhance": True

        }

        self.load()

    # ---------------------------------
    # Load Settings
    # ---------------------------------

    def load(self):

        if os.path.exists(self.file):

            with open(

                self.file,

                "r",

                encoding="utf-8"

            ) as f:

                self.settings.update(

                    json.load(f)

                )

    # ---------------------------------
    # Save Settings
    # ---------------------------------

    def save(self):

        os.makedirs(

            os.path.dirname(self.file),

            exist_ok=True

        )

        with open(

            self.file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                self.settings,

                f,

                indent=4

            )

    # ---------------------------------
    # Get
    # ---------------------------------

    def get(self, key, default=None):

        return self.settings.get(

            key,

            default

        )

    # ---------------------------------
    # Set
    # ---------------------------------

    def set(self, key, value):

        self.settings[key] = value

    # ---------------------------------
    # Camera Settings
    # ---------------------------------

    def camera(self):

        return {

            "id": self.get("camera_id"),

            "width": self.get("camera_width"),

            "height": self.get("camera_height"),

            "fps": self.get("camera_fps")

        }

    # ---------------------------------
    # OCR Settings
    # ---------------------------------

    def ocr(self):

        return {

            "enabled": self.get("ocr_enabled"),

            "language": self.get("ocr_language")

        }

    # ---------------------------------
    # Detection Settings
    # ---------------------------------

    def detection(self):

        return {

            "object_detection":

                self.get("object_detection"),

            "face_recognition":

                self.get("face_recognition"),

            "confidence":

                self.get("confidence")

        }

    # ---------------------------------
    # Reset Default
    # ---------------------------------

    def reset(self):

        self.__init__()

        self.save()

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return self.settings


if __name__ == "__main__":

    settings = VisionSettings()

    print(settings.info())

    settings.save()
    
