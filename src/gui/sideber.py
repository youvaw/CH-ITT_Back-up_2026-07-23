"""
=========================================
CHITT - Sidebar
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import tkinter as tk
from tkinter import ttk


class Sidebar(tk.Frame):

    def __init__(self, master, callback=None):

        super().__init__(master)

        self.callback = callback

        self.configure(

            bg="#252526",

            width=220

        )

        self.pack_propagate(False)

        self.create_widgets()

    # ---------------------------------
    # Create Sidebar
    # ---------------------------------

    def create_widgets(self):

        title = tk.Label(

            self,

            text="CHITT",

            font=("Arial", 20, "bold"),

            bg="#252526",

            fg="white"

        )

        title.pack(

            pady=20

        )

        self.create_button(

            "💬 Chat",

            "chat"

        )

        self.create_button(

            "🎤 Voice",

            "voice"

        )

        self.create_button(

            "👁 Vision",

            "vision"

        )

        self.create_button(

            "🧠 Brain",

            "brain"

        )

        self.create_button(

            "💾 Memory",

            "memory"

        )

        self.create_button(

            "🔌 Plugins",

            "plugins"

        )

        self.create_button(

            "⚙ Settings",

            "settings"

        )

        self.create_button(

            "ℹ About",

            "about"

        )

    # ---------------------------------
    # Sidebar Button
    # ---------------------------------

    def create_button(

        self,

        text,

        page

    ):

        button = ttk.Button(

            self,

            text=text,

            command=lambda: self.open(page)

        )

        button.pack(

            fill="x",

            padx=15,

            pady=5

        )

    # ---------------------------------
    # Open Page
    # ---------------------------------

    def open(self, page):

        print(f"Opening : {page}")

        if self.callback:

            self.callback(page)

    # ---------------------------------
    # Enable
    # ---------------------------------

    def enable(self):

        for widget in self.winfo_children():

            if isinstance(widget, ttk.Button):

                widget.configure(state="normal")

    # ---------------------------------
    # Disable
    # ---------------------------------

    def disable(self):

        for widget in self.winfo_children():

            if isinstance(widget, ttk.Button):

                widget.configure(state="disabled")


if __name__ == "__main__":

    root = tk.Tk()

    root.geometry("250x600")

    sidebar = Sidebar(root)

    sidebar.pack(

        fill="y",

        side="left"

    )

    root.mainloop()
    
