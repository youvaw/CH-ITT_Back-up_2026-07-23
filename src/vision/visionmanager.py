"""
=========================================
CHITT - Vision Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from vision.camera import Camera
from vision.image_capture import ImageCapture
from vision.image_processing import ImageProcessing
from vision.object_detection import ObjectDetection
from vision.face_recognition import FaceRecognition
from vision.ocr import OCR
from vision.screenshot import Screenshot
from vision.image_search import ImageSearch
from vision.vision_settings import VisionSettings


class VisionManager:

    def __init__(self):

        self.camera = Camera()

        self.capture = ImageCapture()

        self.processing = ImageProcessing()

        self.object_detection = ObjectDetection()

        self.face_recognition = FaceRecognition()

        self.ocr = OCR()

        self.screenshot = Screenshot()

        self.image_search = ImageSearch()

        self.settings = VisionSettings()

    # ---------------------------------
    # Start Camera
    # ---------------------------------

    def start_camera(self):

        return self.camera.start()

    # ---------------------------------
    # Stop Camera
    # ---------------------------------

    def stop_camera(self):

        return self.camera.stop()

    # ---------------------------------
    # Capture Image
    # ---------------------------------

    def capture_image(self):

        return self.capture.capture()

    # ---------------------------------
    # Process Image
    # ---------------------------------

    def process_image(self, image):

        return self.processing.process(image)

    # ---------------------------------
    # Detect Objects
    # ---------------------------------

    def detect_objects(self, image):

        return self.object_detection.detect(image)

    # ---------------------------------
    # Recognize Face
    # ---------------------------------

    def recognize_face(self, image):

        return self.face_recognition.recognize(image)

    # ---------------------------------
    # OCR
    # ---------------------------------

    def read_text(self, image):

        return self.ocr.read(image)

    # ---------------------------------
    # Screenshot
    # ---------------------------------

    def capture_screen(self):

        return self.screenshot.capture()

    # ---------------------------------
    # Image Search
    # ---------------------------------

    def search(self, image):

        return self.image_search.search(image)

    # ---------------------------------
    # Status
    # ---------------------------------

    def status(self):

        print("\n===== CHITT VISION =====")

        print("Camera          : Ready")

        print("OCR             : Ready")

        print("Object Detection: Ready")

        print("Face Recognition: Ready")

        print("=========================\n")


if __name__ == "__main__":

    vision = VisionManager()

    vision.status()
    
