"""
=========================================
CHITT - Themes
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class ThemeManager:

    def __init__(self):

        self.current = "dark"

        self.themes = {

            "dark": {

                "background": "#1E1E1E",

                "panel": "#252526",

                "card": "#2D2D30",

                "text": "#FFFFFF",

                "secondary_text": "#C8C8C8",

                "accent": "#00C853",

                "button": "#3C3C3C",

                "button_text": "#FFFFFF",

                "border": "#4D4D4D",

                "status": "#00E676"

            },

            "light": {

                "background": "#F5F5F5",

                "panel": "#FFFFFF",

                "card": "#FAFAFA",

                "text": "#111111",

                "secondary_text": "#555555",

                "accent": "#0078D7",

                "button": "#E0E0E0",

                "button_text": "#000000",

                "border": "#C0C0C0",

                "status": "#009688"

            }

        }

        self.fonts = {

            "title": ("Arial", 20, "bold"),

            "heading": ("Arial", 16, "bold"),

            "normal": ("Arial", 11),

            "small": ("Arial", 9),

            "mono": ("Consolas", 11)

        }

    # ---------------------------------
    # Theme
    # ---------------------------------

    def get(self):

        return self.themes[self.current]

    # ---------------------------------
    # Font
    # ---------------------------------

    def font(self, name):

        return self.fonts.get(

            name,

            self.fonts["normal"]

        )

    # ---------------------------------
    # Change Theme
    # ---------------------------------

    def set(self, theme):

        if theme in self.themes:

            self.current = theme

            return True

        return False

    # ---------------------------------
    # Toggle Theme
    # ---------------------------------

    def toggle(self):

        if self.current == "dark":

            self.current = "light"

        else:

            self.current = "dark"

    # ---------------------------------
    # Background
    # ---------------------------------

    def background(self):

        return self.get()["background"]

    # ---------------------------------
    # Accent
    # ---------------------------------

    def accent(self):

        return self.get()["accent"]

    # ---------------------------------
    # Text
    # ---------------------------------

    def text(self):

        return self.get()["text"]

    # ---------------------------------
    # Button
    # ---------------------------------

    def button(self):

        return {

            "bg": self.get()["button"],

            "fg": self.get()["button_text"]

        }

    # ---------------------------------
    # Theme Info
    # ---------------------------------

    def info(self):

        return {

            "theme": self.current,

            "colors": self.get(),

            "fonts": self.fonts

        }


if __name__ == "__main__":

    theme = ThemeManager()

    print(theme.info())

    theme.toggle()

    print(theme.info())
    
