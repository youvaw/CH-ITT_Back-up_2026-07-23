"""
=========================================
CHITT - Security Environment
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


class SecurityEnvironment:

    def __init__(self):

        self.root = Path.cwd()

        self.os_name = platform.system()

        self.platform = platform.platform()

        self.python = platform.python_version()

        self.machine = platform.machine()

        self.processor = platform.processor()

        self.user = os.getenv("USERNAME") or os.getenv("USER")

    # ---------------------------------
    # Project Root
    # ---------------------------------

    def project_root(self):

        return str(self.root)

    # ---------------------------------
    # Home Directory
    # ---------------------------------

    def home_directory(self):

        return str(Path.home())

    # ---------------------------------
    # Operating System
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
    # Current Working Directory
    # ---------------------------------

    def current_directory(self):

        return os.getcwd()

    # ---------------------------------
    # System Information
    # ---------------------------------

    def system_info(self):

        return {

            "platform": self.platform,

            "os": self.os_name,

            "machine": self.machine,

            "processor": self.processor,

            "python": self.python,

            "python_executable": sys.executable,

            "user": self.user

        }

    # ---------------------------------
    # Check Required Paths
    # ---------------------------------

    def check_paths(self):

        return {

            "security": (self.root / "security").exists(),

            "logs": (self.root / "logs").exists(),

            "keys": (self.root / "security/keys").exists(),

            "storage": (self.root / "security/storage").exists(),

            "certificates": (self.root / "security/certificates").exists()

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "SecurityEnvironment",

            "status": "OK",

            "os": self.os_name,

            "python": self.python

        }


if __name__ == "__main__":

    env = SecurityEnvironment()

    print(env.system_info())

    print(env.check_paths())

    print(env.health())
    
