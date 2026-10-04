"""
=========================================
CHITT - Appearance Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from settings.settingsmanager import SettingsManager


class AppearanceSettings:

    def __init__(self):

        self.settings = SettingsManager()

    # --------------------------
    # Theme
    # --------------------------

    def get_theme(self):

        return self.settings.get("theme")

    def set_theme(self, theme):

        self.settings.set("theme", theme)

    # --------------------------
    # Font Size
    # --------------------------

    def get_font_size(self):

        return self.settings.get("font_size")

    def set_font_size(self, size):

        self.settings.set("font_size", size)

    # --------------------------
    # Window Mode
    # --------------------------

    def get_window_mode(self):

        return self.settings.get("window_mode")

    def set_window_mode(self, mode):

        self.settings.set("window_mode", mode)

    # --------------------------
    # Accent Color
    # --------------------------

    def get_accent_color(self):

        return self.settings.get("accent_color")

    def set_accent_color(self, color):

        self.settings.set("accent_color", color)

    # --------------------------
    # Reset Appearance
    # --------------------------

    def reset(self):

        self.set_theme("dark")
        self.set_font_size(14)
        self.set_window_mode("normal")
        self.set_accent_color("blue")

    # --------------------------
    # Show Appearance Settings
    # --------------------------

    def show(self):

        print("Theme         :", self.get_theme())
        print("Font Size     :", self.get_font_size())
        print("Window Mode   :", self.get_window_mode())
        print("Accent Color  :", self.get_accent_color())


if __name__ == "__main__":

    appearance = AppearanceSettings()

    appearance.show()

