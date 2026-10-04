"""
=========================================
CHITT AI
Brain Package
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

__version__ = "1.0.0"
__author__ = "AVISHKAR"


# Legacy Brain package compatibility.
# The active Brain implementation is:
# src.core.brain


try:
    from .brain_manager import BrainManager
except Exception:
    BrainManager = None


__all__ = [
    "BrainManager",
]
