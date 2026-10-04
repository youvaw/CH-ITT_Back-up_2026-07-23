"""
=========================================
CHITT - Settings Package
=========================================

Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0

Description:
This package manages all CHITT settings,
including voice, AI, appearance, security,
backup, updates, startup, plugins, and more.
=========================================
"""

__version__ = "1.0.0"

__author__ = "AVISHKAR"

from .settingsmanager import SettingsManager

__all__ = [
    "SettingsManager"
]

