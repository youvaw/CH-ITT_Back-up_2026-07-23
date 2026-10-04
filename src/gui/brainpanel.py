import tkinter as tk

class BrainPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        
        lbl = tk.Label(
            self,
            text="🧠 CHITT Brain Panel\n\nLLM Status: Active\nModel: Gemini / Local AI",
            font=("Arial", 16),
            bg="#F5F5F5",
            fg="#202020"
        )
        lbl.pack(expand=True)
        
