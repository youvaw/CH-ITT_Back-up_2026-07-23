"""
CHITT AI
Reasoning Engine
"""


class ReasoningEngine:
    """
    Responsible for logical reasoning.
    """

    def __init__(self):
        self.status = "Ready"

    def reason(self, decision: str) -> str:

        if decision == "GREETING":
            return "Hello! Welcome to CHITT AI."

        elif decision == "TIME":
            return "The user wants to know the current time."

        elif decision == "DATE":
            return "The user wants today's date."

        elif decision == "EXIT":
            return "The user wants to close CHITT."

        return "I don't have enough information to answer that."
