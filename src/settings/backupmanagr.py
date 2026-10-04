"""
=========================================
CHITT - Backup Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import shutil
from datetime import datetime

from settings.settingsmanager import SettingsManager


class BackupManager:

    def __init__(self):

        self.settings = SettingsManager()

    # --------------------------
    # Backup Status
    # --------------------------

    def backup_enabled(self):

        return self.settings.get("auto_backup")

    def enable_backup(self):

        self.settings.set("auto_backup", True)

    def disable_backup(self):

        self.settings.set("auto_backup", False)

    # --------------------------
    # Backup Interval
    # --------------------------

    def get_interval(self):

        return self.settings.get("backup_interval")

    def set_interval(self, interval):

        self.settings.set("backup_interval", interval)

    # --------------------------
    # Create Backup
    # --------------------------

    def create_backup(self, source_folder, backup_folder):

        try:

            if not os.path.exists(backup_folder):

                os.makedirs(backup_folder)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            destination = os.path.join(
                backup_folder,
                f"CHITT_Backup_{timestamp}"
            )

            shutil.copytree(source_folder, destination)

            print("Backup Created Successfully")

            return destination

        except Exception as error:

            print("Backup Failed :", error)

            return None

    # --------------------------
    # Restore Backup
    # --------------------------

    def restore_backup(self, backup_path, destination):

        try:

            if os.path.exists(destination):

                shutil.rmtree(destination)

            shutil.copytree(backup_path, destination)

            print("Backup Restored Successfully")

            return True

        except Exception as error:

            print("Restore Failed :", error)

            return False

    # --------------------------
    # Show Settings
    # --------------------------

    def show(self):

        print("Auto Backup :", self.backup_enabled())

        print("Interval    :", self.get_interval())


if __name__ == "__main__":

    backup = BackupManager()

    backup.show()

