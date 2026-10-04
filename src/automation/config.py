"""
=========================================
CHITT - Automation Configuration
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from pathlib import Path


class AutomationConfig:

    VERSION = "1.0.0"

    MODULE = "Automation"

    ENABLED = True

    # ---------------------------------
    # Keyboard
    # ---------------------------------

    KEYBOARD_DELAY = 0.05

    TYPING_SPEED = "normal"

    # ---------------------------------
    # Mouse
    # ---------------------------------

    MOUSE_DURATION = 0.25

    FAILSAFE = True

    # ---------------------------------
    # Scheduler
    # ---------------------------------

    SCHEDULER_INTERVAL = 30

    # ---------------------------------
    # Clipboard
    # ---------------------------------

    CLIPBOARD_HISTORY = 50

    # ---------------------------------
    # Macro
    # ---------------------------------

    RECORD_MOUSE = True

    RECORD_KEYBOARD = True

    # ---------------------------------
    # Safety
    # ---------------------------------

    CONFIRM_DELETE = True

    CONFIRM_SHUTDOWN = True

    CONFIRM_RESTART = True

    # ---------------------------------
    # Paths
    # ---------------------------------

    ROOT = Path.cwd()

    AUTOMATION = ROOT / "automation"

    MACROS = AUTOMATION / "macros"

    WORKFLOWS = AUTOMATION / "workflows"

    LOGS = ROOT / "logs"

    TEMP = ROOT / "temp"

    # ---------------------------------
    # Create Directories
    # ---------------------------------

    @classmethod
    def initialize(cls):

        cls.AUTOMATION.mkdir(

            parents=True,

            exist_ok=True

        )

        cls.MACROS.mkdir(

            parents=True,

            exist_ok=True

        )

        cls.WORKFLOWS.mkdir(

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
    # Configuration
    # ---------------------------------

    @classmethod
    def info(cls):

        return {

            "module": cls.MODULE,

            "version": cls.VERSION,

            "enabled": cls.ENABLED,

            "automation": str(cls.AUTOMATION),

            "macros": str(cls.MACROS),

            "workflows": str(cls.WORKFLOWS),

            "logs": str(cls.LOGS)

        }


if __name__ == "__main__":

    AutomationConfig.initialize()

    print(

        AutomationConfig.info()

    )
    
