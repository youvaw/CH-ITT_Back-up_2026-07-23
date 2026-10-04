"""
=========================================
CHITT - GUI Package
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from .gui_manager import GUIManager
from .main_window import MainWindow
from .sidebar import Sidebar
from .chat_panel import ChatPanel
from .voice_panel import VoicePanel
from .vision_panel import VisionPanel
from .settings_panel import SettingsPanel
from .status_bar import StatusBar
from .themes import ThemeManager
from .widgets import (
    RoundedButton,
    CardFrame,
    AnimatedLabel,
    ProgressCard,
    ToggleSwitch,
    CustomEntry,
    StatusIndicator,
)
from .splash import SplashScreen
from .tray import TrayManager

__version__ = "1.0.0"

__author__ = "AVISHKAR"

__all__ = [
    "GUIManager",
    "MainWindow",
    "Sidebar",
    "ChatPanel",
    "VoicePanel",
    "VisionPanel",
    "SettingsPanel",
    "StatusBar",
    "ThemeManager",
    "RoundedButton",
    "CardFrame",
    "AnimatedLabel",
    "ProgressCard",
    "ToggleSwitch",
    "CustomEntry",
    "StatusIndicator",
    "SplashScreen",
    "TrayManager",
]
class MainWindow(ctk.CTk):
    def __init__(self, brain=None):
        super().__init__()
        self.brain = brain
        self.title("MAYAX AI - Control Center")
        self.geometry("1000x600")

        # Layout Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1. Sidebar Panel (Left)
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.btn_chat = ctk.CTkButton(self.sidebar_frame, text="💬 Chat", command=lambda: self.show_view("chat"))
        self.btn_chat.pack(pady=10, padx=10)

        self.btn_voice = ctk.CTkButton(self.sidebar_frame, text="🎤 Voice", command=lambda: self.show_view("voice"))
        self.btn_voice.pack(pady=10, padx=10)

        self.btn_vision = ctk.CTkButton(self.sidebar_frame, text="👁 Vision", command=lambda: self.show_view("vision"))
        self.btn_vision.pack(pady=10, padx=10)

        self.btn_memory = ctk.CTkButton(self.sidebar_frame, text="💾 Memory", command=lambda: self.show_view("memory"))
        self.btn_memory.pack(pady=10, padx=10)

        # 2. Main Content Frame (Right)
        self.main_container = ctk.CTkFrame(self)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # 3. Initialize All Views
        self.views = {
            "chat": ChatView(self.main_container, brain=self.brain),
            "voice": VoiceView(self.main_container, brain=self.brain),
            "vision": VisionView(self.main_container),
            "memory": MemoryView(self.main_container)
        }

        # 4. 🔥 Default Tab Active (डीफॉल्ट चॅट स्क्रीन दाखवण्यासाठी)
        self.show_view("chat")

    def show_view(self, view_name):
        """निवडलेला टॅब दाखवणे आणि बाकीचे लपवणे"""
        for name, view in self.views.items():
            if name == view_name:
                view.grid(row=0, column=0, sticky="nsew")
            else:
                view.grid_forget()
                

