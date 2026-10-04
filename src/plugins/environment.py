"""
=========================================
CHITT - Plugin Environment
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import platform
from pathlib import Path


class PluginEnvironment:

    def __init__(self):

        self.project_root = Path.cwd()

        self.plugin_dir = self.project_root / "plugins"

        self.data_dir = self.project_root / "data"

        self.logs_dir = self.project_root / "logs"

        self.temp_dir = self.project_root / "temp"

        self.ensure_directories()

    # ---------------------------------
    # Create Directories
    # ---------------------------------

    def ensure_directories(self):

        for directory in [

            self.plugin_dir,

            self.data_dir,

            self.logs_dir,

            self.temp_dir

        ]:

            directory.mkdir(

                parents=True,

                exist_ok=True

            )

    # ---------------------------------
    # Operating System
    # ---------------------------------

    def operating_system(self):

        return platform.system()

    # ---------------------------------
    # Python Version
    # ---------------------------------

    def python_version(self):

        return platform.python_version()

    # ---------------------------------
    # Computer Name
    # ---------------------------------

    def computer_name(self):

        return platform.node()

    # ---------------------------------
    # Environment Variables
    # ---------------------------------

    def environment(self):

        return dict(os.environ)

    # ---------------------------------
    # Project Paths
    # ---------------------------------

    def paths(self):

        return {

            "project": str(self.project_root),

            "plugins": str(self.plugin_dir),

            "data": str(self.data_dir),

            "logs": str(self.logs_dir),

            "temp": str(self.temp_dir)

        }

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return {

            "os": self.operating_system(),

            "python": self.python_version(),

            "computer": self.computer_name(),

            "paths": self.paths()

        }

    # ---------------------------------
    # Health Check
    # ---------------------------------

    def health(self):

        return {

            "status": "OK",

            "plugin_directory": self.plugin_dir.exists(),

            "data_directory": self.data_dir.exists(),

            "logs_directory": self.logs_dir.exists(),

            "temp_directory": self.temp_dir.exists()

        }


if __name__ == "__main__":

    env = PluginEnvironment()

    print(env.info())

    print(env.health())
    
