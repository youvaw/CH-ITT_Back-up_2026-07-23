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
"""
=========================================
CHITT - Camera
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import cv2


class Camera:

    def __init__(self):

        self.camera = None

        self.camera_id = 0

        self.running = False

    # ---------------------------------
    # Start Camera
    # ---------------------------------

    def start(self):

        if self.running:

            return True

        self.camera = cv2.VideoCapture(self.camera_id)

        if not self.camera.isOpened():

            print("Camera Not Found")

            return False

        self.running = True

        print("Camera Started")

        return True

    # ---------------------------------
    # Read Frame
    # ---------------------------------

    def read(self):

        if not self.running:

            return None

        success, frame = self.camera.read()

        if success:

            return frame

        return None

    # ---------------------------------
    # Show Live Camera
    # ---------------------------------

    def preview(self):

        if not self.start():

            return

        while True:

            frame = self.read()

            if frame is None:

                break

            cv2.imshow("CHITT Camera", frame)

            key = cv2.waitKey(1)

            if key == ord("q"):

                break

        self.stop()

    # ---------------------------------
    # Stop Camera
    # ---------------------------------

    def stop(self):

        if self.camera is not None:

            self.camera.release()

            cv2.destroyAllWindows()

        self.running = False

        print("Camera Stopped")

    # ---------------------------------
    # Camera Status
    # ---------------------------------

    def status(self):

        return self.running

    # ---------------------------------
    # Change Camera
    # ---------------------------------

    def set_camera(self, camera_id):

        self.camera_id = camera_id

    # ---------------------------------
    # Get Camera ID
    # ---------------------------------

    def get_camera(self):

        return self.camera_id


if __name__ == "__main__":

    camera = Camera()

    camera.preview()
    
