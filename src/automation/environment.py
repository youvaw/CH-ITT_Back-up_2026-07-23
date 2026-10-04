"""
=========================================
CHITT - Automation Environment
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import platform
import sys
from pathlib import Path


class AutomationEnvironment:

    def __init__(self):

        self.root = Path.cwd()

        self.os_name = platform.system()

        self.python = platform.python_version()

        self.user = os.getenv("USERNAME") or os.getenv("USER")

    # ---------------------------------
    # Root Path
    # ---------------------------------

    def project_root(self):

        return str(self.root)

    # ---------------------------------
    # OS
    # ---------------------------------

    def operating_system(self):

        return self.os_name

    # ---------------------------------
    # Python Version
    # ---------------------------------

    def python_version(self):

        return self.python

    # ---------------------------------
    # Username
    # ---------------------------------

    def username(self):

        return self.user

    # ---------------------------------
    # Environment Variables
    # ---------------------------------

    def variables(self):

        return dict(os.environ)

    # ---------------------------------
    # Current Directory
    # ---------------------------------

    def current_directory(self):

        return os.getcwd()

    # ---------------------------------
    # Home Directory
    # ---------------------------------

    def home_directory(self):

        return str(Path.home())

    # ---------------------------------
    # System Information
    # ---------------------------------

    def system_info(self):

        return {

            "platform": platform.platform(),

            "machine": platform.machine(),

            "processor": platform.processor(),

            "python": self.python,

            "os": self.os_name,

            "user": self.user

        }

    # ---------------------------------
    # Check Paths
    # ---------------------------------

    def check_paths(self):

        return {

            "automation": (self.root / "automation").exists(),

            "logs": (self.root / "logs").exists(),

            "temp": (self.root / "temp").exists(),

            "workflows": (self.root / "automation/workflows").exists(),

            "macros": (self.root / "automation/macros").exists()

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "AutomationEnvironment",

            "status": "OK",

            "python": self.python,

            "os": self.os_name

        }


if __name__ == "__main__":

    env = AutomationEnvironment()

    print(env.system_info())

    print(env.check_paths())

    print(env.health())
    
