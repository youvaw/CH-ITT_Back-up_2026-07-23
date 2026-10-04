"""
=========================================
CHITT - Core Package
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

__version__ = "1.0.0"

__author__ = "AVISHKAR"

from .engine import Engine
from .startup import Startup
from .shutdown import Shutdown
from .event_manager import EventManager

__all__ = [

    "Engine",

    "Startup",

    "Shutdown",

    "EventManager"

]

