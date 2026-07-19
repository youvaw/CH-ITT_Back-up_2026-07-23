"""
CHITT Vision
Camera Module
"""

import cv2


class Camera:

    def __init__(self, camera_index=0):

        self.camera_index = camera_index
        self.cap = None

    def start(self):

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():

            raise Exception("Camera not found.")

    def read(self):

        success, frame = self.cap.read() # pyright: ignore[reportOptionalMemberAccess]

        if success:
            return frame

        return None

    def stop(self):

        if self.cap:

            self.cap.release()

        cv2.destroyAllWindows()
