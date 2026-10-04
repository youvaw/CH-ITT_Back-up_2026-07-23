"""
=========================================
CHITT - Face Recognition
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import cv2
import face_recognition


class FaceRecognition:

    def __init__(self):

        self.known_faces = []

        self.known_names = []

        self.face_locations = []

        self.face_encodings = []

        self.face_names = []

    # ---------------------------------
    # Load Known Face
    # ---------------------------------

    def load_face(self, image_path, name):

        if not os.path.exists(image_path):

            return False

        image = face_recognition.load_image_file(

            image_path

        )

        encoding = face_recognition.face_encodings(

            image

        )

        if len(encoding) == 0:

            return False

        self.known_faces.append(

            encoding[0]

        )

        self.known_names.append(name)

        return True

    # ---------------------------------
    # Load Folder
    # ---------------------------------

    def load_folder(self, folder):

        if not os.path.exists(folder):

            return

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            name = os.path.splitext(file)[0]

            self.load_face(path, name)

    # ---------------------------------
    # Detect Faces
    # ---------------------------------

    def detect(self, frame):

        rgb = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2RGB

        )

        self.face_locations = face_recognition.face_locations(

            rgb

        )

        self.face_encodings = face_recognition.face_encodings(

            rgb,

            self.face_locations

        )

        return self.face_locations

    # ---------------------------------
    # Face Count
    # ---------------------------------

    def count(self):

        return len(self.face_locations)

    # ---------------------------------
    # Clear Database
    # ---------------------------------

    def clear(self):

        self.known_faces.clear()

        self.known_names.clear()
    # ---------------------------------
    # Recognize Faces
    # ---------------------------------

    def recognize(self, frame):

        self.detect(frame)

        self.face_names = []

        for face_encoding in self.face_encodings:

            matches = face_recognition.compare_faces(

                self.known_faces,

                face_encoding

            )

            name = "Unknown"

            if len(self.known_faces) > 0:

                distances = face_recognition.face_distance(

                    self.known_faces,

                    face_encoding

                )

                best_match = distances.argmin()

                if matches[best_match]:

                    name = self.known_names[best_match]

            self.face_names.append(name)

        return self.face_names

    # ---------------------------------
    # Draw Face Boxes
    # ---------------------------------

    def draw(self, frame):

        for (top, right, bottom, left), name in zip(

            self.face_locations,

            self.face_names

        ):

            cv2.rectangle(

                frame,

                (left, top),

                (right, bottom),

                (0, 255, 0),

                2

            )

            cv2.rectangle(

                frame,

                (left, bottom - 25),

                (right, bottom),

                (0, 255, 0),

                cv2.FILLED

            )

            cv2.putText(

                frame,

                name,

                (left + 5, bottom - 6),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (0, 0, 0),

                1

            )

        return frame

    # ---------------------------------
    # Save Unknown Face
    # ---------------------------------

    def save_unknown(self, frame, path):

        cv2.imwrite(path, frame)

        return path

    # ---------------------------------
    # Live Recognition
    # ---------------------------------

    def live(self):

        camera = cv2.VideoCapture(0)

        while True:

            success, frame = camera.read()

            if not success:

                break

            self.recognize(frame)

            output = self.draw(frame)

            cv2.imshow(

                "CHITT Face Recognition",

                output

            )

            key = cv2.waitKey(1)

            if key == ord("q"):

                break

        camera.release()

        cv2.destroyAllWindows()


if __name__ == "__main__":

    face = FaceRecognition()

    face.load_folder("faces")

    face.live()
            
