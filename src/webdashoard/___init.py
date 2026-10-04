"""
=========================================
CHITT - Web Dashboard
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from .dashboard import Dashboard
from .routes import DashboardRoutes
from .authentication import DashboardAuthentication
from .session_manager import SessionManager
from .widgets import WidgetManager
from .theme import ThemeManager
from .config import DashboardConfig
from .environment import DashboardEnvironment

__author__ = "AVISHKAR"
__version__ = "1.0.0"

__all__ = [

    "Dashboard",

    "DashboardRoutes",

    "DashboardAuthentication",

    "SessionManager",

    "WidgetManager",

    "ThemeManager",

    "DashboardConfig",

    "DashboardEnvironment"

]

