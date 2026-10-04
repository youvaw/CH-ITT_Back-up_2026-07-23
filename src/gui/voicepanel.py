"""
=========================================
CHITT - Voice Panel
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import tkinter as tk
from tkinter import ttk


class VoicePanel(tk.Frame):

    def __init__(self, master):

        super().__init__(master)

        self.configure(bg="#F4F4F4")

        self.listening = False

        self.speaking = False

        self.build()

    # ---------------------------------
    # Build UI
    # ---------------------------------

    def build(self):

        title = tk.Label(

            self,

            text="🎤 Voice Control",

            font=("Arial", 18, "bold"),

            bg="#F4F4F4"

        )

        title.pack(pady=15)

        self.status = tk.Label(

            self,

            text="Status : Idle",

            font=("Arial", 12),

            bg="#F4F4F4",

            fg="blue"

        )

        self.status.pack(pady=10)

        self.wave = tk.Canvas(

            self,

            width=350,

            height=120,

            bg="black",

            highlightthickness=0

        )

        self.wave.pack(pady=20)

        self.draw_wave()

        controls = tk.Frame(

            self,

            bg="#F4F4F4"

        )

        controls.pack(pady=10)

        ttk.Button(

            controls,

            text="🎤 Start",

            command=self.start

        ).grid(row=0, column=0, padx=10)

        ttk.Button(

            controls,

            text="⏹ Stop",

            command=self.stop

        ).grid(row=0, column=1, padx=10)

    # ---------------------------------
    # Draw Fake Wave
    # ---------------------------------

    def draw_wave(self):

        self.wave.delete("all")

        x = 10

        for i in range(40):

            h = 20 if self.listening else 5

            self.wave.create_line(

                x,

                60 - h,

                x,

                60 + h,

                fill="lime",

                width=3

            )

            x += 8

    # ---------------------------------
    # Start Listening
    # ---------------------------------

    def start(self):

        self.listening = True

        self.status.config(

            text="Status : Listening",

            fg="green"

        )

        self.draw_wave()

    # ---------------------------------
    # Stop Listening
    # ---------------------------------

    def stop(self):

        self.listening = False

        self.speaking = False

        self.status.config(

            text="Status : Idle",

            fg="blue"

        )

        self.draw_wave()

    # ---------------------------------
    # Speaking
    # ---------------------------------

    def speaking_on(self):

        self.speaking = True

        self.status.config(

            text="Status : Speaking",

            fg="orange"

        )

    # ---------------------------------
    # Speaking Off
    # ---------------------------------

    def speaking_off(self):

        self.speaking = False

        self.status.config(

            text="Status : Listening",

            fg="green"

        )

    # ---------------------------------
    # Get Status
    # ---------------------------------

    def info(self):

        return {

            "listening": self.listening,

            "speaking": self.speaking

        }


if __name__ == "__main__":

    root = tk.Tk()

    root.title("CHITT Voice")

    root.geometry("500x400")

    panel = VoicePanel(root)

    panel.pack(fill="both", expand=True)

    root.mainloop()
    
