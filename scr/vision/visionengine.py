"""
CHITT Vision Manager
"""

import cv2

from .camera import Camera


class VisionManager:

    def __init__(self):

        self.camera = Camera()

    def start(self):

        self.camera.start()

        while True:

            frame = self.camera.read()

            if frame is None:
                continue

            cv2.imshow("CHITT Vision", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):

                break

        self.camera.stop()
        