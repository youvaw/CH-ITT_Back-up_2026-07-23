"""
=========================================
CHITT - Chat Panel
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class ChatPanel(tk.Frame):

    def __init__(self, master):

        super().__init__(master)

        self.configure(bg="#F4F4F4")

        self.history = []

        self.build()

    # ---------------------------------
    # Build UI
    # ---------------------------------

    def build(self):

        # Chat Area
        self.chat = tk.Text(

            self,

            wrap="word",

            font=("Consolas", 11),

            bg="white",

            fg="black",

            state="disabled"

        )

        scrollbar = ttk.Scrollbar(

            self,

            command=self.chat.yview

        )

        self.chat.configure(

            yscrollcommand=scrollbar.set

        )

        self.chat.pack(

            side="left",

            fill="both",

            expand=True

        )

        scrollbar.pack(

            side="right",

            fill="y"

        )

        # Bottom Area
        bottom = tk.Frame(

            self,

            bg="#EAEAEA"

        )

        bottom.pack(

            fill="x",

            side="bottom"

        )

        self.entry = ttk.Entry(

            bottom,

            font=("Arial", 11)

        )

        self.entry.pack(

            side="left",

            fill="x",

            expand=True,

            padx=5,

            pady=5

        )

        self.entry.bind(

            "<Return>",

            lambda e: self.send()

        )

        ttk.Button(

            bottom,

            text="Send",

            command=self.send

        ).pack(

            side="right",

            padx=5,

            pady=5

        )

    # ---------------------------------
    # Timestamp
    # ---------------------------------

    def time(self):

        return datetime.now().strftime("%H:%M:%S")

    # ---------------------------------
    # Add Message
    # ---------------------------------

    def add_message(

        self,

        sender,

        message

    ):

        self.chat.configure(state="normal")

        self.chat.insert(

            tk.END,

            f"[{self.time()}] {sender}: {message}\n\n"

        )

        self.chat.configure(state="disabled")

        self.chat.see(tk.END)

        self.history.append(

            {

                "sender": sender,

                "message": message,

                "time": self.time()

            }

        )

    # ---------------------------------
    # Send
    # ---------------------------------

    def send(self):

        text = self.entry.get().strip()

        if not text:

            return

        self.add_message(

            "You",

            text

        )

        self.entry.delete(

            0,

            tk.END

        )

        # Placeholder AI response
        self.add_message(

            "CHITT",

            "Message received."

        )

    # ---------------------------------
    # Clear Chat
    # ---------------------------------

    def clear(self):

        self.chat.configure(state="normal")

        self.chat.delete(

            "1.0",

            tk.END

        )

        self.chat.configure(state="disabled")

        self.history.clear()

    # ---------------------------------
    # Get History
    # ---------------------------------

    def get_history(self):

        return self.history


if __name__ == "__main__":

    root = tk.Tk()

    root.title("CHITT Chat")

    root.geometry("700x500")

    panel = ChatPanel(root)

    panel.pack(

        fill="both",

        expand=True

    )

    root.mainloop()
    
