"""
=========================================
CHITT - Update Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from update_system.version_manager import VersionManager
from update_system.package_manager import PackageManager
from update_system.downloader import Downloader
from update_system.installer import Installer
from update_system.rollback import RollbackManager
from update_system.update_checker import UpdateChecker


class UpdateManager:

    def __init__(self):

        self.version = VersionManager()

        self.packages = PackageManager()

        self.downloader = Downloader()

        self.installer = Installer()

        self.rollback = RollbackManager()

        self.checker = UpdateChecker()

        self.active = False

    # ---------------------------------
    # Start
    # ---------------------------------

    def start(self):

        self.active = True

        return {

            "success": True,

            "message": "Update Manager Started"

        }

    # ---------------------------------
    # Stop
    # ---------------------------------

    def stop(self):

        self.active = False

        return {

            "success": True,

            "message": "Update Manager Stopped"

        }

    # ---------------------------------
    # Check Updates
    # ---------------------------------

    def check(self):

        return self.checker.check()

    # ---------------------------------
    # Download Update
    # ---------------------------------

    def download(self, package):

        return self.downloader.download(package)

    # ---------------------------------
    # Install Update
    # ---------------------------------

    def install(self, package):

        return self.installer.install(package)

    # ---------------------------------
    # Rollback
    # ---------------------------------

    def rollback_update(self):

        return self.rollback.rollback()

    # ---------------------------------
    # Current Version
    # ---------------------------------

    def current_version(self):

        return self.version.current()

    # ---------------------------------
    # Latest Version
    # ---------------------------------

    def latest_version(self):

        return self.version.latest()

    # ---------------------------------
    # Update Status
    # ---------------------------------

    def status(self):

        return {

            "active": self.active,

            "current_version": self.current_version()

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "UpdateManager",

            "status": "OK",

            "active": self.active

        }


if __name__ == "__main__":

    manager = UpdateManager()

    manager.start()

    print(manager.health())

    print(manager.status())
    
