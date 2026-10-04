import sys
import os
import tkinter as tk
from tkinter import ttk

# Project Root चा Path सेट करण्यासाठी
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Safe Module Imports
try:
    from src.gui.chatpanel import ChatPanel
except ImportError:
    ChatPanel = None

try:
    from src.gui.voicepanel import VoicePanel
except ImportError:
    VoicePanel = None

try:
    from src.gui.visionpanel import VisionPanel
except ImportError:
    VisionPanel = None

try:
    from src.gui.brainpanel import BrainPanel
except ImportError:
    BrainPanel = None

try:
    from src.gui.memorypanel import MemoryPanel
except ImportError:
    MemoryPanel = None

try:
    from src.gui.settingspanel import SettingsPanel
except ImportError:
    SettingsPanel = None
