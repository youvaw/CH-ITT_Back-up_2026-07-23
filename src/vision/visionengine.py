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
# core/vision_engine.py
import cv2
from vision.camera import Camera  # तुमच्या vision/camera.py चा थेट वापर

class MayaxVisionEngine:
    def __init__(self):
        print("[Vision] Initializing MAYAX Vision Engine...")
        self.camera = Camera()
        self.is_running = False

    def start_feed(self):
        """कॅमेरा सुरू करणे"""
        try:
            self.camera.start()
            self.is_running = True
            print("[Vision] MAYAX Camera Started Successfully.")
            return True
        except Exception as e:
            print(f"[Vision] Camera Start Error: {e}")
            self.is_running = False
            return False

    def get_frame(self):
        """GUI साठी थेट व्हिडिओ फ्रेम मिळवणे"""
        if self.is_running:
            frame = self.camera.read()
            if frame is not None:
                return frame
        return None

    def stop_feed(self):
        """कॅमेरा सुरक्षितपणे बंद करणे"""
        if self.is_running:
            self.is_running = False
            try:
                self.camera.stop()
                print("[Vision] MAYAX Camera Stopped.")
            except Exception as e:
                print(f"[Vision] Camera Stop Error: {e}")
                        
