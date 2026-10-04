"""
=========================================
CHITT - Automation Package
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from .automation_manager import AutomationManager
from .task_runner import TaskRunner
from .workflow import Workflow
from .scheduler import Scheduler
from .app_launcher import AppLauncher
from .keyboard_controller import KeyboardController
from .mouse_controller import MouseController
from .clipboard_manager import ClipboardManager
from .file_manager import FileManager
from .folder_manager import FolderManager
from .process_manager import ProcessManager
from .window_manager import WindowManager
from .hotkeys import HotkeyManager
from .macro_recorder import MacroRecorder
from .macro_player import MacroPlayer
from .automation_settings import AutomationSettings
from .config import AutomationConfig
from .environment import AutomationEnvironment

__author__ = "AVISHKAR"
__version__ = "1.0.0"

__all__ = [

    "AutomationManager",

    "TaskRunner",

    "Workflow",

    "Scheduler",

    "AppLauncher",

    "KeyboardController",

    "MouseController",

    "ClipboardManager",

    "FileManager",

    "FolderManager",

    "ProcessManager",

    "WindowManager",

    "HotkeyManager",

    "MacroRecorder",

    "MacroPlayer",

    "AutomationSettings",

    "AutomationConfig",

    "AutomationEnvironment"

]

