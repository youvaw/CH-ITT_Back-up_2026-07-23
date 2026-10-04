"""
=========================================
CHITT - Installer
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import shutil
from datetime import datetime
from pathlib import Path


class Installer:

    def __init__(self):

        self.install_directory = Path.cwd()

        self.backup_directory = Path(
            "backups"
        )

        self.backup_directory.mkdir(

            parents=True,

            exist_ok=True

        )

    # ---------------------------------
    # Validate Package
    # ---------------------------------

    def validate(self, package_path):

        package = Path(package_path)

        return {

            "success": package.exists(),

            "package": str(package)

        }

    # ---------------------------------
    # Backup Existing File
    # ---------------------------------

    def backup(self, file_path):

        source = Path(file_path)

        if not source.exists():

            return None

        backup_name = (

            source.stem +

            "_" +

            datetime.now().strftime(

                "%Y%m%d_%H%M%S"

            ) +

            source.suffix

        )

        destination = (

            self.backup_directory /

            backup_name

        )

        shutil.copy2(

            source,

            destination

        )

        return str(destination)

    # ---------------------------------
    # Install Package
    # ---------------------------------

    def install(

        self,

        package_path,

        destination=None

    ):

        try:

            package = Path(package_path)

            if not package.exists():

                return {

                    "success": False,

                    "message": "Package not found."

                }

            if destination is None:

                destination = (

                    self.install_directory /

                    package.name

                )

            destination = Path(destination)

            if destination.exists():

                self.backup(destination)

            shutil.copy2(

                package,

                destination

            )

            return {

                "success": True,

                "installed_to": str(destination)

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Remove Installed File
    # ---------------------------------

    def uninstall(self, target):

        try:

            target = Path(target)

            if target.exists():

                target.unlink()

                return {

                    "success": True

                }

            return {

                "success": False,

                "message": "Target not found."

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Installation Status
    # ---------------------------------

    def status(self):

        return {

            "install_directory": str(

                self.install_directory

            ),

            "backup_directory": str(

                self.backup_directory

            )

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "Installer",

            "status": "OK",

            "install_directory": str(

                self.install_directory

            )

        }


if __name__ == "__main__":

    installer = Installer()

    print(installer.health())

    print(installer.status())
    
