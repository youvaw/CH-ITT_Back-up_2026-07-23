"""
=========================================
CHITT - Image Search
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import cv2
import numpy as np
import os


class ImageSearch:

    def __init__(self):

        self.database = {}

        self.orb = cv2.ORB_create(1000)

        self.matcher = cv2.BFMatcher(

            cv2.NORM_HAMMING,

            crossCheck=True

        )

    # ---------------------------------
    # Load Image
    # ---------------------------------

    def load(self, image_path):

        return cv2.imread(image_path)

    # ---------------------------------
    # Feature Extraction
    # ---------------------------------

    def features(self, image):

        gray = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2GRAY

        )

        keypoints, descriptors = self.orb.detectAndCompute(

            gray,

            None

        )

        return keypoints, descriptors

    # ---------------------------------
    # Add Image
    # ---------------------------------

    def add(self, name, image):

        _, descriptor = self.features(image)

        self.database[name] = descriptor

    # ---------------------------------
    # Remove Image
    # ---------------------------------

    def remove(self, name):

        if name in self.database:

            del self.database[name]

    # ---------------------------------
    # Clear Database
    # ---------------------------------

    def clear(self):

        self.database.clear()

    # ---------------------------------
    # Search Image
    # ---------------------------------

    def search(self, image):

        _, query = self.features(image)

        if query is None:

            return None

        best_name = None

        best_score = 0

        for name, descriptor in self.database.items():

            if descriptor is None:

                continue

            matches = self.matcher.match(

                query,

                descriptor

            )

            score = len(matches)

            if score > best_score:

                best_score = score

                best_name = name

        return {

            "image": best_name,

            "score": best_score

        }

    # ---------------------------------
    # Folder Import
    # ---------------------------------

    def load_folder(self, folder):

        if not os.path.exists(folder):

            return

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            image = self.load(path)

            if image is not None:

                self.add(

                    os.path.splitext(file)[0],

                    image

                )

    # ---------------------------------
    # Database Info
    # ---------------------------------

    def info(self):

        return {

            "images": len(self.database)

        }


if __name__ == "__main__":

    engine = ImageSearch()

    engine.load_folder("images")

    query = engine.load("sample.jpg")

    if query is not None:

        print(engine.search(query))

    print(engine.info())
    
