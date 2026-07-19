"""
CHITT AI
Brain Module
"""

from datetime import datetime


class Brain:
    """
    Main Brain of CHITT AI
    """

    def __init__(self):
        self.name = "CHITT AI"
        self.version = "0.1.0"
        self.started = datetime.now()

    def think(self, user_input: str) -> str:

        text = user_input.lower().strip()

        if text == "hello":
            return "Hello! Welcome to CHITT AI."

        elif text == "time":
            return f"Current Time : {datetime.now().strftime('%H:%M:%S')}"

        elif text == "date":
            return f"Today's Date : {datetime.now().strftime('%d-%m-%Y')}"

        elif text == "who are you":
            return "I am CHITT AI."

        else:
            return "I understood your message. My reasoning engine is under development."
                