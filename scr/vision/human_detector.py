"""
CHITT AI
Face Detector
"""

import cv2


class FaceDetector:

    def __init__(self):

        self.face_cascade = cv2.CascadeClassifier( # pyright: ignore[reportAttributeAccessIssue]
            cv2.data.haarcascades + # pyright: ignore[reportAttributeAccessIssue]
            "haarcascade_frontalface_default.xml"
        )

    def detect(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40)
        )

        return faces

    def draw(self, frame, faces):

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        return frame
    