"""
=========================================
CHITT - Package Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from datetime import datetime


class PackageManager:

    def __init__(self):

        self.packages = {}

    # ---------------------------------
    # Register Package
    # ---------------------------------

    def register(

        self,

        name,

        version,

        dependencies=None

    ):

        if dependencies is None:

            dependencies = []

        self.packages[name] = {

            "version": version,

            "dependencies": dependencies,

            "installed": False,

            "installed_on": None

        }

        return {

            "success": True,

            "package": name

        }

    # ---------------------------------
    # Install Package
    # ---------------------------------

    def install(self, name):

        if name not in self.packages:

            return {

                "success": False,

                "message": "Package not found."

            }

        self.packages[name]["installed"] = True

        self.packages[name]["installed_on"] = str(

            datetime.now()

        )

        return {

            "success": True,

            "package": name

        }

    # ---------------------------------
    # Uninstall Package
    # ---------------------------------

    def uninstall(self, name):

        if name not in self.packages:

            return {

                "success": False,

                "message": "Package not found."

            }

        self.packages[name]["installed"] = False

        self.packages[name]["installed_on"] = None

        return {

            "success": True,

            "package": name

        }

    # ---------------------------------
    # Remove Package
    # ---------------------------------

    def remove(self, name):

        if name in self.packages:

            del self.packages[name]

            return True

        return False

    # ---------------------------------
    # Package Exists
    # ---------------------------------

    def exists(self, name):

        return name in self.packages

    # ---------------------------------
    # Package Info
    # ---------------------------------

    def info(self, name):

        return self.packages.get(name)

    # ---------------------------------
    # List Packages
    # ---------------------------------

    def list(self):

        return self.packages

    # ---------------------------------
    # Installed Packages
    # ---------------------------------

    def installed(self):

        return {

            name: data

            for name, data

            in self.packages.items()

            if data["installed"]

        }

    # ---------------------------------
    # Dependencies
    # ---------------------------------

    def dependencies(self, name):

        if name not in self.packages:

            return []

        return self.packages[name]["dependencies"]

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "PackageManager",

            "packages": len(self.packages),

            "installed": len(self.installed()),

            "status": "OK"

        }


if __name__ == "__main__":

    manager = PackageManager()

    manager.register(

        "Vision",

        "1.0.0",

        ["OpenCV", "NumPy"]

    )

    manager.install("Vision")

    print(manager.list())

    print(manager.health())
    
