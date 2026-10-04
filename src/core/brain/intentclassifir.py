"""
=========================================
CHITT - Intent Classifier
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class IntentClassifier:

    def __init__(self):

        self.intents = {

            "web": [
                "google",
                "youtube",
                "github",
                "website",
                "browser",
                "search"
            ],

            "app": [
                "notepad",
                "calculator",
                "paint",
                "chrome",
                "vscode",
                "explorer"
            ],

            "system": [
                "shutdown",
                "restart",
                "sleep",
                "lock",
                "logout"
            ],

            "media": [
                "music",
                "song",
                "video",
                "pause",
                "resume",
                "next",
                "previous"
            ],

            "file": [
                "create file",
                "delete file",
                "rename file",
                "copy file",
                "move file"
            ],

            "settings": [
                "settings",
                "voice",
                "theme",
                "language",
                "volume",
                "update"
            ]

        }

    # ---------------------------------

    def detect(self, command):

        command = command.lower()

        for intent, keywords in self.intents.items():

            for keyword in keywords:

                if keyword in command:

                    return intent

        return "unknown"

    # ---------------------------------

    def add_intent(self, intent_name, keywords):

        self.intents[intent_name] = keywords

    # ---------------------------------

    def show_intents(self):

        for intent in self.intents:

            print(intent)


if __name__ == "__main__":

    classifier = IntentClassifier()

    print(classifier.detect("Open YouTube"))

    print(classifier.detect("Open Calculator"))

    print(classifier.detect("Shutdown PC"))

    print(classifier.detect("Play Music"))

    print(classifier.detect("Open Settings"))
    
