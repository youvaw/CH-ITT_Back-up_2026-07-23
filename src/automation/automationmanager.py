"""
=========================================
CHITT - Automation Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from automation.task_runner import TaskRunner
from automation.workflow import Workflow
from automation.scheduler import Scheduler
from automation.app_launcher import AppLauncher
from automation.keyboard_controller import KeyboardController
from automation.mouse_controller import MouseController
from automation.clipboard_manager import ClipboardManager
from automation.file_manager import FileManager
from automation.folder_manager import FolderManager
from automation.process_manager import ProcessManager
from automation.window_manager import WindowManager
from automation.hotkeys import HotkeyManager
from automation.macro_recorder import MacroRecorder
from automation.macro_player import MacroPlayer


class AutomationManager:

    def __init__(self):

        self.task_runner = TaskRunner()

        self.workflow = Workflow()

        self.scheduler = Scheduler()

        self.app_launcher = AppLauncher()

        self.keyboard = KeyboardController()

        self.mouse = MouseController()

        self.clipboard = ClipboardManager()

        self.file_manager = FileManager()

        self.folder_manager = FolderManager()

        self.process_manager = ProcessManager()

        self.window_manager = WindowManager()

        self.hotkeys = HotkeyManager()

        self.macro_recorder = MacroRecorder()

        self.macro_player = MacroPlayer()

        self.running = False

    # ---------------------------------
    # Start Automation
    # ---------------------------------

    def start(self):

        self.running = True

        self.scheduler.start()

        print("Automation Started")

    # ---------------------------------
    # Stop Automation
    # ---------------------------------

    def stop(self):

        self.running = False

        self.scheduler.stop()

        print("Automation Stopped")

    # ---------------------------------
    # Execute Task
    # ---------------------------------

    def execute_task(self, task):

        return self.task_runner.run(task)

    # ---------------------------------
    # Execute Workflow
    # ---------------------------------

    def execute_workflow(self, workflow):

        return self.workflow.execute(workflow)

    # ---------------------------------
    # Launch Application
    # ---------------------------------

    def launch(self, app):

        return self.app_launcher.launch(app)

    # ---------------------------------
    # Clipboard
    # ---------------------------------

    def copy(self, text):

        return self.clipboard.copy(text)

    def paste(self):

        return self.clipboard.paste()

    # ---------------------------------
    # File
    # ---------------------------------

    def open_file(self, path):

        return self.file_manager.open(path)

    # ---------------------------------
    # Folder
    # ---------------------------------

    def open_folder(self, path):

        return self.folder_manager.open(path)

    # ---------------------------------
    # Status
    # ---------------------------------

    def status(self):

        return {

            "running": self.running,

            "scheduler": self.scheduler.status(),

            "clipboard": "Ready",

            "keyboard": "Ready",

            "mouse": "Ready"

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "Automation",

            "status": "OK",

            "running": self.running

        }


if __name__ == "__main__":

    manager = AutomationManager()

    manager.start()

    print(manager.health())

    manager.stop()
    
