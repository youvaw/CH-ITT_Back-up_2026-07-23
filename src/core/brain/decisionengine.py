"""
=========================================
CHITT - Decision Engine
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class DecisionEngine:

    def __init__(self):

        self.routes = {

            "web": "commands.web_commands",

            "app": "commands.app_commands",

            "system": "commands.system_commands",

            "media": "commands.media_commands",

            "file": "commands.file_commands",

            "settings": "settings.settings_manager",

            "memory": "memory.memory_manager",

            "vision": "vision.vision_manager",

            "voice": "voice.voice_manager",

            "brain": "brain.brain_manager",

            "plugin": "plugins.plugin_manager",

            "unknown": "response.default"

        }

    # ---------------------------------
    # Decide Module
    # ---------------------------------

    def make(self, intent):

        if intent in self.routes:

            return {

                "intent": intent,

                "module": self.routes[intent],

                "status": "success"

            }

        return {

            "intent": "unknown",

            "module": self.routes["unknown"],

            "status": "failed"

        }

    # ---------------------------------
    # Add New Route
    # ---------------------------------

    def add_route(self, intent, module):

        self.routes[intent] = module

    # ---------------------------------
    # Remove Route
    # ---------------------------------

    def remove_route(self, intent):

        if intent in self.routes:

            del self.routes[intent]

    # ---------------------------------
    # Check Route
    # ---------------------------------

    def exists(self, intent):

        return intent in self.routes

    # ---------------------------------
    # Get Module
    # ---------------------------------

    def get_module(self, intent):

        return self.routes.get(intent)

    # ---------------------------------
    # Show Routes
    # ---------------------------------

    def show_routes(self):

        for intent, module in self.routes.items():

            print(f"{intent} -> {module}")


if __name__ == "__main__":

    engine = DecisionEngine()

    print(engine.make("web"))

    print(engine.make("settings"))

    print(engine.make("system"))

    print(engine.make("unknown"))
    
