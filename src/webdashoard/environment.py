"""
=========================================
CHITT - Web Dashboard Environment
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import platform
import socket
import sys
from pathlib import Path


class DashboardEnvironment:

    def __init__(self):

        self.root = Path.cwd()

        self.os_name = platform.system()

        self.platform = platform.platform()

        self.python = platform.python_version()

        self.hostname = socket.gethostname()

        self.ip = self._get_ip()

        self.user = (

            os.getenv("USERNAME")

            or os.getenv("USER")

        )

    # ---------------------------------
    # Get Local IP
    # ---------------------------------

    def _get_ip(self):

        try:

            return socket.gethostbyname(

                self.hostname

            )

        except Exception:

            return "127.0.0.1"

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
    # Environment Variables
    # ---------------------------------

    def variables(self):

        return dict(os.environ)

    # ---------------------------------
    # System Information
    # ---------------------------------

    def system_info(self):

        return {

            "hostname": self.hostname,

            "ip": self.ip,

            "platform": self.platform,

            "os": self.os_name,

            "python": self.python,

            "python_executable":
                sys.executable,

            "user": self.user

        }

    # ---------------------------------
    # Check Dashboard Paths
    # ---------------------------------

    def check_paths(self):

        return {

            "dashboard":
                (
                    self.root
                    / "web_dashboard"
                ).exists(),

            "static":
                (
                    self.root
                    / "web_dashboard"
                    / "static"
                ).exists(),

            "templates":
                (
                    self.root
                    / "web_dashboard"
                    / "templates"
                ).exists(),

            "logs":
                (
                    self.root
                    / "logs"
                ).exists(),

            "temp":
                (
                    self.root
                    / "temp"
                ).exists()

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module":
                "DashboardEnvironment",

            "status":
                "OK",

            "hostname":
                self.hostname,

            "ip":
                self.ip,

            "python":
                self.python

        }


if __name__ == "__main__":

    environment = DashboardEnvironment()

    print(

        environment.system_info()

    )

    print(

        environment.check_paths()

    )

    print(

        environment.health()

    )
    
