"""
=========================================
CHITT - OCR Engine
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import cv2
import pytesseract


class OCR:

    def __init__(self):

        self.language = "eng"

        self.config = "--oem 3 --psm 6"

    # ---------------------------------
    # Set Language
    # ---------------------------------

    def set_language(self, language):

        self.language = language

    # ---------------------------------
    # Set Config
    # ---------------------------------

    def set_config(self, config):

        self.config = config

    # ---------------------------------
    # Read Image
    # ---------------------------------

    def load(self, image_path):

        return cv2.imread(image_path)

    # ---------------------------------
    # Gray Image
    # ---------------------------------

    def grayscale(self, image):

        return cv2.cvtColor(

            image,

            cv2.COLOR_BGR2GRAY

        )

    # ---------------------------------
    # Threshold
    # ---------------------------------

    def threshold(self, image):

        gray = self.grayscale(image)

        _, binary = cv2.threshold(

            gray,

            150,

            255,

            cv2.THRESH_BINARY

        )

        return binary

    # ---------------------------------
    # OCR From Image
    # ---------------------------------

    def read(self, image):

        processed = self.threshold(image)

        text = pytesseract.image_to_string(

            processed,

            lang=self.language,

            config=self.config

        )

        return text.strip()

    # ---------------------------------
    # OCR From File
    # ---------------------------------

    def read_file(self, image_path):

        image = self.load(image_path)

        if image is None:

            return ""

        return self.read(image)
    # ---------------------------------
    # OCR Data
    # ---------------------------------

    def data(self, image):

        processed = self.threshold(image)

        return pytesseract.image_to_data(

            processed,

            lang=self.language,

            config=self.config,

            output_type=pytesseract.Output.DICT

        )

    # ---------------------------------
    # Draw OCR Boxes
    # ---------------------------------

    def draw(self, image):

        data = self.data(image)

        total = len(data["text"])

        for i in range(total):

            text = data["text"][i].strip()

            confidence = int(float(data["conf"][i]))

            if confidence > 50 and text != "":

                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]

                cv2.rectangle(

                    image,

                    (x, y),

                    (x + w, y + h),

                    (0, 255, 0),

                    2

                )

                cv2.putText(

                    image,

                    text,

                    (x, y - 5),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.5,

                    (0, 255, 0),

                    1

                )

        return image

    # ---------------------------------
    # Save OCR Result
    # ---------------------------------

    def save_text(self, image, file_name):

        text = self.read(image)

        with open(

            file_name,

            "w",

            encoding="utf-8"

        ) as file:

            file.write(text)

        return file_name

    # ---------------------------------
    # Live Camera OCR
    # ---------------------------------

    def live(self):

        camera = cv2.VideoCapture(0)

        while True:

            success, frame = camera.read()

            if not success:

                break

            output = self.draw(frame)

            cv2.imshow(

                "CHITT OCR",

                output

            )

            key = cv2.waitKey(1)

            if key == ord("q"):

                break

        camera.release()

        cv2.destroyAllWindows()

    # ---------------------------------
    # OCR Information
    # ---------------------------------

    def info(self):

        return {

            "language": self.language,

            "config": self.config

        }


if __name__ == "__main__":

    ocr = OCR()

    image = ocr.load("sample.jpg")

    if image is not None:

        print(ocr.read(image))

        result = ocr.draw(image)

        cv2.imshow("OCR", result)

        cv2.waitKey(0)

        cv2.destroyAllWindows()
            
