"""
=========================================
CHITT - GUI Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import tkinter as tk
from tkinter import ttk


class GUIManager:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("CHITT AI")

        self.root.geometry("1200x700")

        self.root.configure(bg="#1e1e1e")

        self.create_ui()

    # ---------------------------------
    # Create UI
    # ---------------------------------

    def create_ui(self):

        self.header = tk.Label(

            self.root,

            text="CHITT AI Assistant",

            font=("Arial", 20, "bold"),

            bg="#1e1e1e",

            fg="white"

        )

        self.header.pack(pady=10)

        self.status = tk.Label(

            self.root,

            text="Status : Ready",

            bg="#1e1e1e",

            fg="lightgreen"

        )

        self.status.pack()

        self.chat_box = tk.Text(

            self.root,

            width=100,

            height=25,

            bg="#2d2d2d",

            fg="white"

        )

        self.chat_box.pack(pady=10)

        self.input_box = tk.Entry(

            self.root,

            width=80

        )

        self.input_box.pack(side="left", padx=10)

        self.send_button = ttk.Button(

            self.root,

            text="Send",

            command=self.send

        )

        self.send_button.pack(side="left")

    # ---------------------------------
    # Send Message
    # ---------------------------------

    def send(self):

        message = self.input_box.get()

        if message:

            self.chat_box.insert(

                tk.END,

                f"\nYou : {message}\n"

            )

            self.input_box.delete(0, tk.END)

    # ---------------------------------
    # Start GUI
    # ---------------------------------

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    gui = GUIManager()

    gui.run()
    
