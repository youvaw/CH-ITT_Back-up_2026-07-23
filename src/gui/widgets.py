"""
=========================================
CHITT - Custom Widgets
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import tkinter as tk
from tkinter import ttk


# =========================================
# Rounded Button
# =========================================

class RoundedButton(ttk.Button):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)


# =========================================
# Card Frame
# =========================================

class CardFrame(tk.Frame):

    def __init__(

        self,

        master,

        title="",

        **kwargs

    ):

        super().__init__(

            master,

            bg="white",

            bd=1,

            relief="solid",

            **kwargs

        )

        self.title = tk.Label(

            self,

            text=title,

            font=("Arial", 12, "bold"),

            bg="white"

        )

        self.title.pack(

            anchor="w",

            padx=10,

            pady=8

        )


# =========================================
# Animated Label
# =========================================

class AnimatedLabel(tk.Label):

    def __init__(

        self,

        master,

        **kwargs

    ):

        super().__init__(master, **kwargs)

        self.texts = []

        self.index = 0

    def set_messages(self, messages):

        self.texts = messages

        self.index = 0

        self.animate()

    def animate(self):

        if not self.texts:

            return

        self.config(

            text=self.texts[self.index]

        )

        self.index = (

            self.index + 1

        ) % len(self.texts)

        self.after(

            1200,

            self.animate

        )


# =========================================
# Progress Card
# =========================================

class ProgressCard(CardFrame):

    def __init__(

        self,

        master,

        title="Progress"

    ):

        super().__init__(

            master,

            title

        )

        self.bar = ttk.Progressbar(

            self,

            length=250,

            mode="determinate"

        )

        self.bar.pack(

            padx=10,

            pady=10

        )

    def set(self, value):

        self.bar["value"] = value


# =========================================
# Toggle Switch
# =========================================

class ToggleSwitch(ttk.Checkbutton):

    def __init__(

        self,

        master,

        text="",

        **kwargs

    ):

        self.state = tk.BooleanVar()

        super().__init__(

            master,

            text=text,

            variable=self.state,

            **kwargs

        )

    def get(self):

        return self.state.get()

    def set(self, value):

        self.state.set(value)


# =========================================
# Custom Entry
# =========================================

class CustomEntry(ttk.Entry):

    def __init__(

        self,

        master,

        **kwargs

    ):

        super().__init__(

            master,

            **kwargs

        )

    def value(self):

        return self.get()


# =========================================
# Status Indicator
# =========================================

class StatusIndicator(tk.Frame):

    def __init__(

        self,

        master,

        text="Status"

    ):

        super().__init__(master)

        self.dot = tk.Canvas(

            self,

            width=14,

            height=14,

            highlightthickness=0

        )

        self.dot.pack(

            side="left"

        )

        self.label = tk.Label(

            self,

            text=text

        )

        self.label.pack(

            side="left",

            padx=5

        )

        self.set("gray")

    def set(self, color):

        self.dot.delete("all")

        self.dot.create_oval(

            2,

            2,

            12,

            12,

            fill=color,

            outline=color

        )


# =========================================
# Demo
# =========================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title("CHITT Widgets")

    card = CardFrame(root, "Demo Card")
    card.pack(padx=20, pady=10)

    progress = ProgressCard(root)
    progress.pack(padx=20, pady=10)
    progress.set(65)

    toggle = ToggleSwitch(root, text="Enable")
    toggle.pack(pady=10)

    status = StatusIndicator(root, "Voice")
    status.pack(pady=10)
    status.set("green")

    root.mainloop()
    
