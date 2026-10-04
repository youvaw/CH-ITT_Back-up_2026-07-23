"""
=========================================
CHITT - Image Processing
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import cv2
import numpy as np


class ImageProcessing:

    def __init__(self):

        pass

    # ---------------------------------
    # Read Image
    # ---------------------------------

    def load(self, image_path):

        return cv2.imread(image_path)

    # ---------------------------------
    # Save Image
    # ---------------------------------

    def save(self, image, path):

        cv2.imwrite(path, image)

        return path

    # ---------------------------------
    # Resize
    # ---------------------------------

    def resize(self, image, width, height):

        return cv2.resize(

            image,

            (width, height)

        )

    # ---------------------------------
    # Rotate
    # ---------------------------------

    def rotate(self, image, angle):

        h, w = image.shape[:2]

        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(

            center,

            angle,

            1.0

        )

        return cv2.warpAffine(

            image,

            matrix,

            (w, h)

        )

    # ---------------------------------
    # Crop
    # ---------------------------------

    def crop(

        self,

        image,

        x,

        y,

        width,

        height

    ):

        return image[

            y:y + height,

            x:x + width

        ]

    # ---------------------------------
    # Flip
    # ---------------------------------

    def flip_horizontal(self, image):

        return cv2.flip(image, 1)

    def flip_vertical(self, image):

        return cv2.flip(image, 0)

    # ---------------------------------
    # Gray
    # ---------------------------------

    def grayscale(self, image):

        return cv2.cvtColor(

            image,

            cv2.COLOR_BGR2GRAY

        )

    # ---------------------------------
    # Blur
    # ---------------------------------

    def blur(self, image, size=5):

        return cv2.GaussianBlur(

            image,

            (size, size),

            0

        )

    # ---------------------------------
    # Median Blur
    # ---------------------------------

    def median(self, image, size=5):

        return cv2.medianBlur(

            image,

            size

        )

    # ---------------------------------
    # Sharpen
    # ---------------------------------

    def sharpen(self, image):

        kernel = np.array([

            [-1, -1, -1],

            [-1,  9, -1],

            [-1, -1, -1]

        ])

        return cv2.filter2D(

            image,

            -1,

            kernel

        )

    # ---------------------------------
    # Brightness
    # ---------------------------------

    def brightness(

        self,

        image,

        value=30

    ):

        return cv2.convertScaleAbs(

            image,

            beta=value

        )

    # ---------------------------------
    # Contrast
    # ---------------------------------

    def contrast(

        self,

        image,

        alpha=1.5

    ):

        return cv2.convertScaleAbs(

            image,

            alpha=alpha,

            beta=0

        )

    # ---------------------------------
    # Negative
    # ---------------------------------

    def negative(self, image):

        return cv2.bitwise_not(image)
    # ---------------------------------
    # Edge Detection
    # ---------------------------------

    def edges(self, image):

        gray = self.grayscale(image)

        return cv2.Canny(

            gray,

            100,

            200

        )

    # ---------------------------------
    # Binary Threshold
    # ---------------------------------

    def threshold(

        self,

        image,

        value=127

    ):

        gray = self.grayscale(image)

        _, result = cv2.threshold(

            gray,

            value,

            255,

            cv2.THRESH_BINARY

        )

        return result

    # ---------------------------------
    # Adaptive Threshold
    # ---------------------------------

    def adaptive_threshold(self, image):

        gray = self.grayscale(image)

        return cv2.adaptiveThreshold(

            gray,

            255,

            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

            cv2.THRESH_BINARY,

            11,

            2

        )

    # ---------------------------------
    # Noise Removal
    # ---------------------------------

    def denoise(self, image):

        return cv2.fastNlMeansDenoisingColored(

            image,

            None,

            10,

            10,

            7,

            21

        )

    # ---------------------------------
    # Dilate
    # ---------------------------------

    def dilate(self, image):

        kernel = np.ones((3, 3), np.uint8)

        return cv2.dilate(

            image,

            kernel,

            iterations=1

        )

    # ---------------------------------
    # Erode
    # ---------------------------------

    def erode(self, image):

        kernel = np.ones((3, 3), np.uint8)

        return cv2.erode(

            image,

            kernel,

            iterations=1

        )

    # ---------------------------------
    # RGB Convert
    # ---------------------------------

    def rgb(self, image):

        return cv2.cvtColor(

            image,

            cv2.COLOR_BGR2RGB

        )

    # ---------------------------------
    # BGR Convert
    # ---------------------------------

    def bgr(self, image):

        return cv2.cvtColor(

            image,

            cv2.COLOR_RGB2BGR

        )

    # ---------------------------------
    # Histogram Equalization
    # ---------------------------------

    def equalize(self, image):

        gray = self.grayscale(image)

        return cv2.equalizeHist(gray)

    # ---------------------------------
    # Auto Enhancement
    # ---------------------------------

    def enhance(self, image):

        image = self.denoise(image)

        image = self.contrast(image)

        image = self.sharpen(image)

        return image

    # ---------------------------------
    # Show Image
    # ---------------------------------

    def show(

        self,

        title,

        image

    ):

        cv2.imshow(title, image)

        cv2.waitKey(0)

        cv2.destroyAllWindows()

    # ---------------------------------
    # Complete Processing
    # ---------------------------------

    def process(self, image):

        image = self.enhance(image)

        return image


if __name__ == "__main__":

    processor = ImageProcessing()

    image = processor.load("sample.jpg")

    if image is not None:

        output = processor.process(image)

        processor.show("CHITT", output)
            
