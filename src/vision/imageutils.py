"""
=========================================
CHITT - Image Utilities
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import cv2
import numpy as np


class ImageUtils:

    def __init__(self):

        pass

    # ---------------------------------
    # Load Image
    # ---------------------------------

    def load(self, path):

        return cv2.imread(path)

    # ---------------------------------
    # Save Image
    # ---------------------------------

    def save(self, image, path):

        cv2.imwrite(path, image)

        return path

    # ---------------------------------
    # File Exists
    # ---------------------------------

    def exists(self, path):

        return os.path.exists(path)

    # ---------------------------------
    # File Size
    # ---------------------------------

    def file_size(self, path):

        if not self.exists(path):

            return 0

        return os.path.getsize(path)

    # ---------------------------------
    # Image Size
    # ---------------------------------

    def image_size(self, image):

        h, w = image.shape[:2]

        return {

            "width": w,

            "height": h

        }

    # ---------------------------------
    # Resize Keep Ratio
    # ---------------------------------

    def resize_ratio(self, image, width):

        h, w = image.shape[:2]

        ratio = width / w

        height = int(h * ratio)

        return cv2.resize(

            image,

            (width, height)

        )

    # ---------------------------------
    # RGB
    # ---------------------------------

    def rgb(self, image):

        return cv2.cvtColor(

            image,

            cv2.COLOR_BGR2RGB

        )

    # ---------------------------------
    # BGR
    # ---------------------------------

    def bgr(self, image):

        return cv2.cvtColor(

            image,

            cv2.COLOR_RGB2BGR

        )

    # ---------------------------------
    # Histogram
    # ---------------------------------

    def histogram(self, image):

        gray = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2GRAY

        )

        return cv2.calcHist(

            [gray],

            [0],

            None,

            [256],

            [0, 256]

        )

    # ---------------------------------
    # Compress
    # ---------------------------------

    def compress(

        self,

        image,

        path,

        quality=80

    ):

        cv2.imwrite(

            path,

            image,

            [

                cv2.IMWRITE_JPEG_QUALITY,

                quality

            ]

        )

        return path

    # ---------------------------------
    # Image Info
    # ---------------------------------

    def info(self, image):

        h, w = image.shape[:2]

        return {

            "width": w,

            "height": h,

            "channels": image.shape[2]

            if len(image.shape) == 3

            else 1,

            "dtype": str(image.dtype)

        }

    # ---------------------------------
    # Convert PNG
    # ---------------------------------

    def png(self, image, path):

        cv2.imwrite(path, image)

        return path

    # ---------------------------------
    # Convert JPG
    # ---------------------------------

    def jpg(self, image, path):

        cv2.imwrite(path, image)

        return path

    # ---------------------------------
    # Delete Image
    # ---------------------------------

    def delete(self, path):

        if self.exists(path):

            os.remove(path)

            return True

        return False


if __name__ == "__main__":

    utils = ImageUtils()

    img = utils.load("sample.jpg")

    if img is not None:

        print(utils.info(img))
        
