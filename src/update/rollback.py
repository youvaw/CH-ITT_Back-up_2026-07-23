"""
=========================================
CHITT - Rollback Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import shutil
from pathlib import Path
from datetime import datetime


class RollbackManager:

    def __init__(self):

        self.backup_directory = Path("backups")

        self.restore_directory = Path.cwd()

        self.backup_directory.mkdir(

            parents=True,

            exist_ok=True

        )

    # ---------------------------------
    # List Backups
    # ---------------------------------

    def backups(self):

        return sorted(

            [

                file.name

                for file in self.backup_directory.iterdir()

                if file.is_file()

            ]

        )

    # ---------------------------------
    # Latest Backup
    # ---------------------------------

    def latest(self):

        items = self.backups()

        if not items:

            return None

        return items[-1]

    # ---------------------------------
    # Restore Backup
    # ---------------------------------

    def rollback(self, backup_name=None):

        try:

            if backup_name is None:

                backup_name = self.latest()

            if backup_name is None:

                return {

                    "success": False,

                    "message": "No backup available."

                }

            source = self.backup_directory / backup_name

            destination = (

                self.restore_directory /

                Path(backup_name).name.split("_")[0]

            )

            shutil.copy2(

                source,

                destination

            )

            return {

                "success": True,

                "restored": str(destination)

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Delete Backup
    # ---------------------------------

    def delete(self, backup_name):

        file = self.backup_directory / backup_name

        if file.exists():

            file.unlink()

            return True

        return False

    # ---------------------------------
    # Clear All Backups
    # ---------------------------------

    def clear(self):

        for file in self.backup_directory.iterdir():

            if file.is_file():

                file.unlink()

        return True

    # ---------------------------------
    # Backup Information
    # ---------------------------------

    def info(self):

        return {

            "count": len(self.backups()),

            "latest": self.latest(),

            "directory": str(self.backup_directory)

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "RollbackManager",

            "status": "OK",

            "backups": len(self.backups())

        }


if __name__ == "__main__":

    rollback = RollbackManager()

    print(rollback.health())

    print(rollback.info())
    
