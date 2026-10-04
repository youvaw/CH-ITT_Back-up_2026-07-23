"""
=========================================
CHITT - Update Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from settings.settingsmanager import SettingsManager


class UpdateManager:

    def __init__(self):

        self.settings = SettingsManager()

    # --------------------------
    # Auto Update
    # --------------------------

    def auto_update_enabled(self):

        return self.settings.get("auto_update")

    def enable_auto_update(self):

        self.settings.set("auto_update", True)

    def disable_auto_update(self):

        self.settings.set("auto_update", False)

    # --------------------------
    # Check Update On Startup
    # --------------------------

    def startup_check_enabled(self):

        return self.settings.get("check_update_on_startup")

    def enable_startup_check(self):

        self.settings.set("check_update_on_startup", True)

    def disable_startup_check(self):

        self.settings.set("check_update_on_startup", False)

    # --------------------------
    # Current Version
    # --------------------------

    def current_version(self):

        return self.settings.get("assistant_version")

    # --------------------------
    # Update Version
    # --------------------------

    def update_version(self, version):

        self.settings.set("assistant_version", version)

    # --------------------------
    # Check For Update
    # --------------------------

    def check_update(self):

        print("Checking for updates...")

        return False

    # --------------------------
    # Install Update
    # --------------------------

    def install_update(self):

        print("Installing update...")

        return True

    # --------------------------
    # Show Update Settings
    # --------------------------

    def show(self):

        print("Current Version :", self.current_version())
        print("Auto Update     :", self.auto_update_enabled())
        print("Startup Check   :", self.startup_check_enabled())


if __name__ == "__main__":

    update = UpdateManager()

    update.show()

