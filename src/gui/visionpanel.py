"""
=========================================
CHITT - Vision Panel
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import tkinter as tk
from tkinter import ttk

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


class VisionPanel(tk.Frame):

    def __init__(self, master):

        super().__init__(master)

        self.configure(bg="#F4F4F4")

        self.camera_running = False

        self.object_count = 0

        self.face_count = 0

        self.build()

    # ---------------------------------
    # Build UI
    # ---------------------------------

    def build(self):

        title = tk.Label(

            self,

            text="👁 CHITT Vision",

            font=("Arial", 18, "bold"),

            bg="#F4F4F4"

        )

        title.pack(pady=10)

        self.preview = tk.Label(

            self,

            text="Camera Preview",

            width=70,

            height=20,

            bg="black",

            fg="white",

            relief="sunken"

        )

        self.preview.pack(pady=10)

        info = tk.Frame(

            self,

            bg="#F4F4F4"

        )

        info.pack(fill="x", padx=20)

        self.camera_label = tk.Label(

            info,

            text="Camera : OFF",

            bg="#F4F4F4",

            fg="red"

        )

        self.camera_label.pack(anchor="w")

        self.face_label = tk.Label(

            info,

            text="Faces : 0",

            bg="#F4F4F4"

        )

        self.face_label.pack(anchor="w")

        self.object_label = tk.Label(

            info,

            text="Objects : 0",

            bg="#F4F4F4"

        )

        self.object_label.pack(anchor="w")

        controls = tk.Frame(

            self,

            bg="#F4F4F4"

        )

        controls.pack(pady=15)

        ttk.Button(

            controls,

            text="📷 Start Camera",

            command=self.start_camera

        ).grid(row=0, column=0, padx=5)

        ttk.Button(

            controls,

            text="⏹ Stop Camera",

            command=self.stop_camera

        ).grid(row=0, column=1, padx=5)

        ttk.Button(

            controls,

            text="📸 Screenshot",

            command=self.capture

        ).grid(row=0, column=2, padx=5)

    # ---------------------------------
    # Start Camera
    # ---------------------------------

    def start_camera(self):

        self.camera_running = True

        self.camera_label.config(

            text="Camera : ON",

            fg="green"

        )

    # ---------------------------------
    # Stop Camera
    # ---------------------------------

    def stop_camera(self):

        self.camera_running = False

        self.camera_label.config(

            text="Camera : OFF",

            fg="red"

        )

    # ---------------------------------
    # Screenshot
    # ---------------------------------

    def capture(self):

        print("Screenshot Captured")

    # ---------------------------------
    # Update Face Count
    # ---------------------------------

    def update_faces(self, count):

        self.face_count = count

        self.face_label.config(

            text=f"Faces : {count}"

        )

    # ---------------------------------
    # Update Object Count
    # ---------------------------------

    def update_objects(self, count):

        self.object_count = count

        self.object_label.config(

            text=f"Objects : {count}"

        )

    # ---------------------------------
    # Update Preview Image
    # ---------------------------------

    def update_image(self, frame):

        if Image is None:

            return

        image = Image.fromarray(frame)

        image = image.resize((640, 360))

        photo = ImageTk.PhotoImage(image)

        self.preview.configure(image=photo, text="")

        self.preview.image = photo

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return {

            "camera": self.camera_running,

            "faces": self.face_count,

            "objects": self.object_count

        }


if __name__ == "__main__":

    root = tk.Tk()

    root.title("CHITT Vision")

    root.geometry("800x650")

    panel = VisionPanel(root)

    panel.pack(fill="both", expand=True)

    root.mainloop()
    
