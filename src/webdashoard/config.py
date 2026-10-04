"""
=========================================
CHITT - Web Dashboard Configuration
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from pathlib import Path


class DashboardConfig:

    VERSION = "1.0.0"

    MODULE = "WebDashboard"

    ENABLED = True

    # ---------------------------------
    # Server
    # ---------------------------------

    HOST = "127.0.0.1"

    PORT = 8080

    DEBUG = False

    RELOAD = False

    # ---------------------------------
    # Dashboard
    # ---------------------------------

    TITLE = "CHITT Dashboard"

    THEME = "dark"

    DEFAULT_LANGUAGE = "en"

    SESSION_TIMEOUT = 3600

    # ---------------------------------
    # Features
    # ---------------------------------

    CHAT_ENABLED = True

    VOICE_ENABLED = True

    VISION_ENABLED = True

    MEMORY_ENABLED = True

    AUTOMATION_ENABLED = True

    LOGS_ENABLED = True

    SYSTEM_MONITOR_ENABLED = True

    # ---------------------------------
    # Paths
    # ---------------------------------

    ROOT = Path.cwd()

    DASHBOARD = ROOT / "web_dashboard"

    STATIC = DASHBOARD / "static"

    TEMPLATES = DASHBOARD / "templates"

    LOGS = ROOT / "logs"

    TEMP = ROOT / "temp"

    # ---------------------------------
    # Initialize Directories
    # ---------------------------------

    @classmethod
    def initialize(cls):

        cls.DASHBOARD.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.STATIC.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.TEMPLATES.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.LOGS.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.TEMP.mkdir(
            parents=True,
            exist_ok=True
        )

    # ---------------------------------
    # Feature Status
    # ---------------------------------

    @classmethod
    def features(cls):

        return {

            "chat": cls.CHAT_ENABLED,

            "voice": cls.VOICE_ENABLED,

            "vision": cls.VISION_ENABLED,

            "memory": cls.MEMORY_ENABLED,

            "automation": cls.AUTOMATION_ENABLED,

            "logs": cls.LOGS_ENABLED,

            "system_monitor":
                cls.SYSTEM_MONITOR_ENABLED

        }

    # ---------------------------------
    # Configuration Information
    # ---------------------------------

    @classmethod
    def info(cls):

        return {

            "module": cls.MODULE,

            "version": cls.VERSION,

            "enabled": cls.ENABLED,

            "host": cls.HOST,

            "port": cls.PORT,

            "title": cls.TITLE,

            "theme": cls.THEME,

            "language":
                cls.DEFAULT_LANGUAGE,

            "features":
                cls.features()

        }


if __name__ == "__main__":

    DashboardConfig.initialize()

    print(DashboardConfig.info())
    
