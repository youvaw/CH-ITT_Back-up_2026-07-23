"""
=========================================
CHITT - Dashboard Widget Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class WidgetManager:

    def __init__(self):

        self.widgets = {}

    # ---------------------------------
    # Register Widget
    # ---------------------------------

    def register(

        self,

        name,

        widget

    ):

        if not name:

            raise ValueError(

                "Widget name is required."

            )

        self.widgets[name] = widget

        return True

    # ---------------------------------
    # Remove Widget
    # ---------------------------------

    def remove(self, name):

        if name in self.widgets:

            del self.widgets[name]

            return True

        return False

    # ---------------------------------
    # Get Widget
    # ---------------------------------

    def get(self, name):

        return self.widgets.get(name)

    # ---------------------------------
    # Check Widget
    # ---------------------------------

    def exists(self, name):

        return name in self.widgets

    # ---------------------------------
    # List Widgets
    # ---------------------------------

    def list(self):

        return list(

            self.widgets.keys()

        )

    # ---------------------------------
    # Clear Widgets
    # ---------------------------------

    def clear(self):

        self.widgets.clear()

    # ---------------------------------
    # Count
    # ---------------------------------

    def count(self):

        return len(self.widgets)

    # ---------------------------------
    # Dashboard Widgets
    # ---------------------------------

    def register_defaults(self):

        defaults = {

            "chat": {

                "title": "Chat",

                "type": "chat"

            },

            "voice": {

                "title": "Voice",

                "type": "voice"

            },

            "vision": {

                "title": "Vision",

                "type": "vision"

            },

            "memory": {

                "title": "Memory",

                "type": "memory"

            },

            "automation": {

                "title": "Automation",

                "type": "automation"

            },

            "system": {

                "title": "System Monitor",

                "type": "system"

            },

            "logs": {

                "title": "Logs",

                "type": "logs"

            }

        }

        for name, widget in defaults.items():

            self.register(

                name,

                widget

            )

    # ---------------------------------
    # Export
    # ---------------------------------

    def export(self):

        return dict(self.widgets)

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module":
                "WidgetManager",

            "widgets":
                self.count(),

            "status":
                "OK"

        }


if __name__ == "__main__":

    manager = WidgetManager()

    manager.register_defaults()

    print(manager.export())

    print(manager.health())
    
