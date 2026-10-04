"""
=========================================
CHITT - Response Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class ResponseManager:

    def __init__(self):

        self.responses = {

            "web": "Opening your web request.",

            "app": "Opening application.",

            "system": "Executing system command.",

            "media": "Media command executed.",

            "file": "File operation completed.",

            "settings": "Opening settings.",

            "memory": "Memory updated.",

            "vision": "Vision system activated.",

            "voice": "Voice settings updated.",

            "brain": "Brain module activated.",

            "plugin": "Plugin executed.",

            "success": "Done.",

            "failed": "Sorry, I couldn't complete your request.",

            "unknown": "Sorry, I don't understand that command."
        }

    # ---------------------------------
    # Generate Response
    # ---------------------------------

    def generate(self, decision):

        if isinstance(decision, dict):

            intent = decision.get("intent", "unknown")

            status = decision.get("status", "failed")

            if status == "success":

                return self.responses.get(
                    intent,
                    self.responses["success"]
                )

            return self.responses["failed"]

        return self.responses["unknown"]

    # ---------------------------------
    # Add Response
    # ---------------------------------

    def add_response(self, key, message):

        self.responses[key] = message

    # ---------------------------------
    # Remove Response
    # ---------------------------------

    def remove_response(self, key):

        if key in self.responses:

            del self.responses[key]

    # ---------------------------------
    # Get Response
    # ---------------------------------

    def get(self, key):

        return self.responses.get(
            key,
            self.responses["unknown"]
        )

    # ---------------------------------
    # Show Responses
    # ---------------------------------

    def show(self):

        for key, value in self.responses.items():

            print(f"{key} : {value}")


if __name__ == "__main__":


    manager = ResponseManager()

    decision = {

        "intent": "web",

        "status": "success"

    }

    print(manager.generate(decision))
