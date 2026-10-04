"""
=========================================
CHITT - Vision Configuration
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os

# =========================================
# VERSION
# =========================================

VISION_VERSION = "1.0.0"

# =========================================
# ROOT PATH
# =========================================

VISION_ROOT = os.path.dirname(__file__)

# =========================================
# DATA PATHS
# =========================================

CONFIG_PATH = os.path.join(

    VISION_ROOT,

    "config.json"

)

MODEL_PATH = os.path.join(

    VISION_ROOT,

    "models"

)

DATASET_PATH = os.path.join(

    VISION_ROOT,

    "dataset"

)

IMAGE_PATH = os.path.join(

    VISION_ROOT,

    "images"

)

SCREENSHOT_PATH = os.path.join(

    VISION_ROOT,

    "screenshots"

)

FACE_PATH = os.path.join(

    VISION_ROOT,

    "faces"

)

# =========================================
# YOLO MODEL
# =========================================

YOLO_CFG = os.path.join(

    MODEL_PATH,

    "yolov4.cfg"

)

YOLO_WEIGHTS = os.path.join(

    MODEL_PATH,

    "yolov4.weights"

)

YOLO_CLASSES = os.path.join(

    MODEL_PATH,

    "coco.names"

)

# =========================================
# CAMERA
# =========================================

DEFAULT_CAMERA = 0

CAMERA_WIDTH = 1280

CAMERA_HEIGHT = 720

CAMERA_FPS = 30

# =========================================
# OCR
# =========================================

OCR_LANGUAGE = "eng"

OCR_CONFIG = "--oem 3 --psm 6"

# =========================================
# FACE RECOGNITION
# =========================================

FACE_TOLERANCE = 0.60

FACE_MODEL = "hog"

# =========================================
# DETECTION
# =========================================

CONFIDENCE = 0.50

NMS_THRESHOLD = 0.40

# =========================================
# IMAGE
# =========================================

DEFAULT_IMAGE_FORMAT = ".png"

JPEG_QUALITY = 90

PNG_COMPRESSION = 3

# =========================================
# SCREENSHOT
# =========================================

SCREENSHOT_FORMAT = ".png"

# =========================================
# IMAGE PROCESSING
# =========================================

BLUR_SIZE = 5

SHARPEN = True

AUTO_ENHANCE = True

# =========================================
# DISPLAY
# =========================================

SHOW_PREVIEW = True

SHOW_BOXES = True

SHOW_LABELS = True

# =========================================
# SAVE OPTIONS
# =========================================

SAVE_IMAGES = True

SAVE_SCREENSHOTS = True

SAVE_UNKNOWN_FACE = True

# =========================================
# SUPPORTED FORMATS
# =========================================

SUPPORTED_FORMATS = [

    ".jpg",

    ".jpeg",

    ".png",

    ".bmp",

    ".tiff",

    ".webp"

]

# =========================================
# CREATE REQUIRED FOLDERS
# =========================================

REQUIRED_FOLDERS = [

    MODEL_PATH,

    DATASET_PATH,

    IMAGE_PATH,

    SCREENSHOT_PATH,

    FACE_PATH

]

for folder in REQUIRED_FOLDERS:

    os.makedirs(

        folder,

        exist_ok=True

    )
    
