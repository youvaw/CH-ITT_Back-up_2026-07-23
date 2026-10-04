import tkinter as tk

class MemoryPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        
        lbl = tk.Label(
            self,
            text="💾 CHITT Memory Panel\n\nContext & History Logs",
            font=("Arial", 16),
            bg="#F5F5F5",
            fg="#202020"
        )
        lbl.pack(expand=True)
