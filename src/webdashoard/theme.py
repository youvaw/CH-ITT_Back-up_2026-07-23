"""
=========================================
CHITT - Dashboard Theme Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class ThemeManager:

    def __init__(self):

        self.themes = {

            "light": {

                "background": "#ffffff",

                "foreground": "#111111",

                "primary": "#2563eb",

                "secondary": "#64748b",

                "surface": "#f8fafc",

                "border": "#e2e8f0"

            },

            "dark": {

                "background": "#0f172a",

                "foreground": "#f8fafc",

                "primary": "#3b82f6",

                "secondary": "#94a3b8",

                "surface": "#1e293b",

                "border": "#334155"

            }

        }

        self.current_theme = "dark"

    # ---------------------------------
    # Register Theme
    # ---------------------------------

    def register(

        self,

        name,

        theme

    ):

        if not name:

            raise ValueError(

                "Theme name is required."

            )

        if not isinstance(theme, dict):

            raise TypeError(

                "Theme must be a dictionary."

            )

        self.themes[name] = theme

        return True

    # ---------------------------------
    # Set Theme
    # ---------------------------------

    def set_theme(self, name):

        if name not in self.themes:

            return False

        self.current_theme = name

        return True

    # ---------------------------------
    # Get Current Theme
    # ---------------------------------

    def current(self):

        return self.themes.get(

            self.current_theme

        )

    # ---------------------------------
    # Get Theme
    # ---------------------------------

    def get(self, name):

        return self.themes.get(name)

    # ---------------------------------
    # List Themes
    # ---------------------------------

    def list(self):

        return list(

            self.themes.keys()

        )

    # ---------------------------------
    # Current Theme Name
    # ---------------------------------

    def current_name(self):

        return self.current_theme

    # ---------------------------------
    # Remove Theme
    # ---------------------------------

    def remove(self, name):

        if name in (

            "light",

            "dark"

        ):

            return False

        if name in self.themes:

            del self.themes[name]

            if self.current_theme == name:

                self.current_theme = "dark"

            return True

        return False

    # ---------------------------------
    # Export
    # ---------------------------------

    def export(self):

        return {

            "current":

                self.current_theme,

            "themes":

                dict(self.themes)

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module":
                "ThemeManager",

            "current":
                self.current_theme,

            "themes":
                len(self.themes),

            "status":
                "OK"

        }


if __name__ == "__main__":

    manager = ThemeManager()

    print(manager.current())

    manager.set_theme("light")

    print(manager.current())

    print(manager.health())
    
