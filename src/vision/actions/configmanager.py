"""
=========================================
CHITT - Vision Config Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from vision.config_loader import ConfigLoader
from vision.config import *


class ConfigManager:

    def __init__(self):

        self.loader = ConfigLoader()

        self.loader.load()

    # ---------------------------------
    # Get Setting
    # ---------------------------------

    def get(self, key, default=None):

        return self.loader.get(key, default)

    # ---------------------------------
    # Set Setting
    # ---------------------------------

    def set(self, key, value):

        self.loader.set(key, value)

    # ---------------------------------
    # Save
    # ---------------------------------

    def save(self):

        self.loader.save()

    # ---------------------------------
    # Reload
    # ---------------------------------

    def reload(self):

        self.loader.reload()

    # ---------------------------------
    # Camera
    # ---------------------------------

    def camera(self):

        return {

            "id": self.get(

                "camera_id",

                DEFAULT_CAMERA

            ),

            "width": self.get(

                "camera_width",

                CAMERA_WIDTH

            ),

            "height": self.get(

                "camera_height",

                CAMERA_HEIGHT

            ),

            "fps": self.get(

                "camera_fps",

                CAMERA_FPS

            )

        }

    # ---------------------------------
    # OCR
    # ---------------------------------

    def ocr(self):

        return {

            "language": self.get(

                "ocr_language",

                OCR_LANGUAGE

            ),

            "config": OCR_CONFIG

        }

    # ---------------------------------
    # Detection
    # ---------------------------------

    def detection(self):

        return {

            "confidence": self.get(

                "confidence",

                CONFIDENCE

            ),

            "nms": NMS_THRESHOLD

        }

    # ---------------------------------
    # Face Recognition
    # ---------------------------------

    def face(self):

        return {

            "tolerance": FACE_TOLERANCE,

            "model": FACE_MODEL

        }

    # ---------------------------------
    # Image
    # ---------------------------------

    def image(self):

        return {

            "format": DEFAULT_IMAGE_FORMAT,

            "quality": JPEG_QUALITY,

            "enhance": AUTO_ENHANCE

        }

    # ---------------------------------
    # Display
    # ---------------------------------

    def display(self):

        return {

            "preview": SHOW_PREVIEW,

            "boxes": SHOW_BOXES,

            "labels": SHOW_LABELS

        }

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return {

            "version": VISION_VERSION,

            "config_file": CONFIG_PATH,

            "supported": SUPPORTED_FORMATS

        }


if __name__ == "__main__":

    manager = ConfigManager()

    print(manager.info())

    print(manager.camera())

    print(manager.ocr())
    
