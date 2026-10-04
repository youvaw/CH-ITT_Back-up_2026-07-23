"""
=========================================
CHITT - Update Checker
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import requests
from update_system.version_manager import VersionManager


class UpdateChecker:

    def __init__(self):

        self.version_manager = VersionManager()

        self.update_url = (
            "https://example.com/chitt/version.json"
        )

    # ---------------------------------
    # Set Update URL
    # ---------------------------------

    def set_url(self, url):

        self.update_url = url

    # ---------------------------------
    # Check Remote Version
    # ---------------------------------

    def check(self):

        try:

            response = requests.get(

                self.update_url,

                timeout=10

            )

            response.raise_for_status()

            data = response.json()

            latest = data.get(

                "version",

                self.version_manager.current()

            )

            self.version_manager.set_latest(

                latest

            )

            return {

                "success": True,

                "current":

                    self.version_manager.current(),

                "latest":

                    latest,

                "status":

                    self.version_manager.compare()

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Update Available
    # ---------------------------------

    def available(self):

        return (

            self.version_manager.compare()

            == "UPDATE_AVAILABLE"

        )

    # ---------------------------------
    # Current Version
    # ---------------------------------

    def current(self):

        return self.version_manager.current()

    # ---------------------------------
    # Latest Version
    # ---------------------------------

    def latest(self):

        return self.version_manager.latest()

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "UpdateChecker",

            "current":

                self.current(),

            "latest":

                self.latest(),

            "status": "OK"

        }


if __name__ == "__main__":

    checker = UpdateChecker()

    print(checker.health())

    print(checker.check())
    
