"""
=========================================
CHITT - Settings Panel
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import tkinter as tk
from tkinter import ttk


class SettingsPanel(tk.Frame):

    def __init__(self, master):

        super().__init__(master)

        self.configure(bg="#F4F4F4")

        self.build()

    # ---------------------------------
    # Build UI
    # ---------------------------------

    def build(self):

        title = tk.Label(

            self,

            text="⚙ CHITT Settings",

            font=("Arial", 18, "bold"),

            bg="#F4F4F4"

        )

        title.pack(pady=15)

        notebook = ttk.Notebook(self)

        notebook.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )

        # ------------------------------

        voice = tk.Frame(notebook)

        vision = tk.Frame(notebook)

        memory = tk.Frame(notebook)

        system = tk.Frame(notebook)

        notebook.add(voice, text="Voice")

        notebook.add(vision, text="Vision")

        notebook.add(memory, text="Memory")

        notebook.add(system, text="System")

        # ---------------------------------
        # Voice Settings
        # ---------------------------------

        self.voice_enable = tk.BooleanVar(value=True)

        self.voice_speed = tk.IntVar(value=180)

        ttk.Checkbutton(

            voice,

            text="Enable Voice",

            variable=self.voice_enable

        ).pack(anchor="w", pady=5)

        ttk.Label(

            voice,

            text="Speech Speed"

        ).pack(anchor="w")

        ttk.Scale(

            voice,

            from_=100,

            to=250,

            variable=self.voice_speed,

            orient="horizontal"

        ).pack(fill="x")

        # ---------------------------------
        # Vision Settings
        # ---------------------------------

        self.camera_enable = tk.BooleanVar(value=True)

        self.object_detection = tk.BooleanVar(value=True)

        self.face_detection = tk.BooleanVar(value=True)

        ttk.Checkbutton(

            vision,

            text="Enable Camera",

            variable=self.camera_enable

        ).pack(anchor="w", pady=5)

        ttk.Checkbutton(

            vision,

            text="Object Detection",

            variable=self.object_detection

        ).pack(anchor="w", pady=5)

        ttk.Checkbutton(

            vision,

            text="Face Recognition",

            variable=self.face_detection

        ).pack(anchor="w", pady=5)

        # ---------------------------------
        # Memory Settings
        # ---------------------------------

        self.memory_enable = tk.BooleanVar(value=True)

        ttk.Checkbutton(

            memory,

            text="Enable Memory",

            variable=self.memory_enable

        ).pack(anchor="w", pady=5)

        # ---------------------------------
        # System Settings
        # ---------------------------------

        self.dark_mode = tk.BooleanVar(value=True)

        self.auto_start = tk.BooleanVar(value=False)

        ttk.Checkbutton(

            system,

            text="Dark Mode",

            variable=self.dark_mode

        ).pack(anchor="w", pady=5)

        ttk.Checkbutton(

            system,

            text="Start with Windows",

            variable=self.auto_start

        ).pack(anchor="w", pady=5)

        # ---------------------------------
        # Save Button
        # ---------------------------------

        ttk.Button(

            self,

            text="💾 Save Settings",

            command=self.save

        ).pack(pady=10)

    # ---------------------------------
    # Save Settings
    # ---------------------------------

    def save(self):

        print("Settings Saved")

    # ---------------------------------
    # Export Settings
    # ---------------------------------

    def values(self):

        return {

            "voice": self.voice_enable.get(),

            "speed": self.voice_speed.get(),

            "camera": self.camera_enable.get(),

            "object_detection":

                self.object_detection.get(),

            "face_detection":

                self.face_detection.get(),

            "memory":

                self.memory_enable.get(),

            "dark_mode":

                self.dark_mode.get(),

            "auto_start":

                self.auto_start.get()

        }


if __name__ == "__main__":

    root = tk.Tk()

    root.title("CHITT Settings")

    root.geometry("700x500")

    panel = SettingsPanel(root)

    panel.pack(fill="both", expand=True)

    root.mainloop()
    
