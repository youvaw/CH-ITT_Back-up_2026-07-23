"""
=========================================
CHITT - Object Detection
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import cv2
import os


class ObjectDetection:

    def __init__(self):

        self.model = None

        self.classes = []

        self.net = None

        self.confidence = 0.50

        self.nms_threshold = 0.40

    # ---------------------------------
    # Load Class Names
    # ---------------------------------

    def load_classes(self, class_file):

        if not os.path.exists(class_file):

            return False

        with open(class_file, "r") as file:

            self.classes = [

                line.strip()

                for line in file.readlines()

            ]

        return True

    # ---------------------------------
    # Load YOLO Model
    # ---------------------------------

    def load_model(

        self,

        weights,

        config

    ):

        if not os.path.exists(weights):

            return False

        if not os.path.exists(config):

            return False

        self.net = cv2.dnn.readNet(

            weights,

            config

        )

        return True

    # ---------------------------------
    # Get Output Layers
    # ---------------------------------

    def output_layers(self):

        layer_names = self.net.getLayerNames()

        output = [

            layer_names[i - 1]

            for i in self.net.getUnconnectedOutLayers().flatten()

        ]

        return output

    # ---------------------------------
    # Set Confidence
    # ---------------------------------

    def set_confidence(self, value):

        self.confidence = value

    # ---------------------------------
    # Get Confidence
    # ---------------------------------

    def get_confidence(self):

        return self.confidence

    # ---------------------------------
    # Create Blob
    # ---------------------------------

    def blob(self, image):

        return cv2.dnn.blobFromImage(

            image,

            scalefactor=1 / 255,

            size=(416, 416),

            swapRB=True,

            crop=False

        )

    # ---------------------------------
    # Detect Objects
    # ---------------------------------

    def detect(self, image):

        if self.net is None:

            return []

        blob = self.blob(image)

        self.net.setInput(blob)

        outputs = self.net.forward(

            self.output_layers()

        )

        return outputs
    # ---------------------------------
    # Process Detection
    # ---------------------------------

    def process(self, image):

        outputs = self.detect(image)

        height, width = image.shape[:2]

        boxes = []

        confidences = []

        class_ids = []

        for output in outputs:

            for detection in output:

                scores = detection[5:]

                class_id = scores.argmax()

                confidence = scores[class_id]

                if confidence > self.confidence:

                    center_x = int(detection[0] * width)

                    center_y = int(detection[1] * height)

                    w = int(detection[2] * width)

                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)

                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])

                    confidences.append(float(confidence))

                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(

            boxes,

            confidences,

            self.confidence,

            self.nms_threshold

        )

        results = []

        if len(indexes) > 0:

            for i in indexes.flatten():

                x, y, w, h = boxes[i]

                label = self.classes[class_ids[i]]

                score = confidences[i]

                results.append({

                    "label": label,

                    "confidence": score,

                    "box": (x, y, w, h)

                })

        return results

    # ---------------------------------
    # Draw Detection
    # ---------------------------------

    def draw(self, image, detections):

        for obj in detections:

            x, y, w, h = obj["box"]

            label = obj["label"]

            score = obj["confidence"]

            cv2.rectangle(

                image,

                (x, y),

                (x + w, y + h),

                (0, 255, 0),

                2

            )

            text = f"{label} {score:.2f}"

            cv2.putText(

                image,

                text,

                (x, y - 10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.5,

                (0, 255, 0),

                2

            )

        return image

    # ---------------------------------
    # Object Count
    # ---------------------------------

    def count(self, detections):

        return len(detections)

    # ---------------------------------
    # Show Image
    # ---------------------------------

    def show(self, image):

        cv2.imshow("CHITT Object Detection", image)

        cv2.waitKey(0)

        cv2.destroyAllWindows()


if __name__ == "__main__":

    detector = ObjectDetection()

    detector.load_classes("models/coco.names")

    detector.load_model(

        "models/yolov4.weights",

        "models/yolov4.cfg"

    )

    image = cv2.imread("sample.jpg")

    detections = detector.process(image)

    output = detector.draw(image, detections)

    detector.show(output)

    print("Objects Found :", detector.count(detections))
        
