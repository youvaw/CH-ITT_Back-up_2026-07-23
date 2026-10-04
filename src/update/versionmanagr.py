"""
=========================================
CHITT - Version Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from datetime import datetime


class VersionManager:

    def __init__(self):

        self.current_version = "1.0.0"

        self.latest_version = "1.0.0"

        self.history = [

            {

                "version": "1.0.0",

                "date": str(datetime.now()),

                "notes": "Initial Release"

            }

        ]

    # ---------------------------------
    # Current Version
    # ---------------------------------

    def current(self):

        return self.current_version

    # ---------------------------------
    # Latest Version
    # ---------------------------------

    def latest(self):

        return self.latest_version

    # ---------------------------------
    # Set Latest Version
    # ---------------------------------

    def set_latest(self, version):

        self.latest_version = version

    # ---------------------------------
    # Compare Versions
    # ---------------------------------

    def compare(self):

        current = tuple(

            map(

                int,

                self.current_version.split(".")

            )

        )

        latest = tuple(

            map(

                int,

                self.latest_version.split(".")

            )

        )

        if latest > current:

            return "UPDATE_AVAILABLE"

        elif latest == current:

            return "UP_TO_DATE"

        else:

            return "DEVELOPMENT_VERSION"

    # ---------------------------------
    # Update Current Version
    # ---------------------------------

    def update(self, version, notes=""):

        self.current_version = version

        self.history.append(

            {

                "version": version,

                "date": str(datetime.now()),

                "notes": notes

            }

        )

        return True

    # ---------------------------------
    # Version History
    # ---------------------------------

    def get_history(self):

        return self.history

    # ---------------------------------
    # Last Version
    # ---------------------------------

    def previous(self):

        if len(self.history) >= 2:

            return self.history[-2]

        return None

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "VersionManager",

            "current": self.current_version,

            "latest": self.latest_version,

            "status": "OK"

        }


if __name__ == "__main__":

    manager = VersionManager()

    print(manager.health())

    print(manager.compare())
    
