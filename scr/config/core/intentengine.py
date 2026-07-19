"""
CHITT AI
Intent Engine
"""

import re


class IntentEngine:

    def detect(self, command: str):

        command = command.lower().strip()

        intents = {

            "open_google": [
                r"open google",
                r"google open",
                r"launch google"
            ],

            "open_youtube": [
                r"open youtube",
                r"youtube open",
                r"launch youtube"
            ],

            "open_notepad": [
                r"open notepad",
                r"start notepad"
            ],

            "open_calculator": [
                r"open calculator",
                r"start calculator"
            ],

            "time": [
                r"time",
                r"what is the time",
                r"current time"
            ],

            "date": [
                r"date",
                r"today date",
                r"current date"
            ],

            "battery": [
                r"battery",
                r"battery status",
                r"battery percentage"
            ]
        }

        for intent, patterns in intents.items():

            for pattern in patterns:

                if re.search(pattern, command):

                    return intent

        return "chat"
    