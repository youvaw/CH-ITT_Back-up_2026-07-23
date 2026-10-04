"""
=========================================
CHITT - Security Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from settings.settingsmanager import SettingsManager


class SecuritySettings:

    def __init__(self):

        self.settings = SettingsManager()

    # --------------------------
    # Password Protection
    # --------------------------

    def password_enabled(self):

        return self.settings.get("password_enabled")

    def enable_password(self):

        self.settings.set("password_enabled", True)

    def disable_password(self):

        self.settings.set("password_enabled", False)

    # --------------------------
    # Password
    # --------------------------

    def get_password(self):

        return self.settings.get("password")

    def set_password(self, password):

        self.settings.set("password", password)

    # --------------------------
    # Developer Mode
    # --------------------------

    def developer_mode(self):

        return self.settings.get("developer_mode")

    def enable_developer_mode(self):

        self.settings.set("developer_mode", True)

    def disable_developer_mode(self):

        self.settings.set("developer_mode", False)

    # --------------------------
    # Reset Security
    # --------------------------

    def reset(self):

        self.disable_password()
        self.set_password("")
        self.disable_developer_mode()

    # --------------------------
    # Show Settings
    # --------------------------

    def show(self):

        print("Password Enabled :", self.password_enabled())
        print("Developer Mode   :", self.developer_mode())


if __name__ == "__main__":

    security = SecuritySettings()

    security.show()

