"""
=========================================
CHITT - Status Bar
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import tkinter as tk
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None


class StatusBar(tk.Frame):

    def __init__(self, master):

        super().__init__(master)

        self.configure(

            bg="#202020",

            height=28

        )

        self.pack_propagate(False)

        self.build()

        self.update_status()

    # ---------------------------------
    # Build
    # ---------------------------------

    def build(self):

        self.label = tk.Label(

            self,

            bg="#202020",

            fg="white",

            anchor="w",

            font=("Arial", 10)

        )

        self.label.pack(

            fill="both",

            expand=True,

            padx=10

        )

    # ---------------------------------
    # CPU
    # ---------------------------------

    def cpu(self):

        if psutil:

            return psutil.cpu_percent()

        return 0

    # ---------------------------------
    # RAM
    # ---------------------------------

    def ram(self):

        if psutil:

            return psutil.virtual_memory().percent

        return 0

    # ---------------------------------
    # Time
    # ---------------------------------

    def clock(self):

        return datetime.now().strftime(

            "%H:%M:%S"

        )

    # ---------------------------------
    # Update Status
    # ---------------------------------

    def update_status(self):

        text = (

            f"Voice: Ready   "

            f"Vision: Ready   "

            f"CPU: {self.cpu()}%   "

            f"RAM: {self.ram()}%   "

            f"Time: {self.clock()}"

        )

        self.label.config(text=text)

        self.after(

            1000,

            self.update_status

        )

    # ---------------------------------
    # Custom Status
    # ---------------------------------

    def set(self, message):

        self.label.config(text=message)


if __name__ == "__main__":

    root = tk.Tk()

    root.geometry("900x60")

    bar = StatusBar(root)

    bar.pack(

        fill="x",

        side="bottom"

    )

    root.mainloop()
    
