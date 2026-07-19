"""
CHITT AI
Decision Engine
"""


class DecisionEngine:
    """
    Responsible for selecting the best action
    based on user input.
    """

    def __init__(self):
        self.status = "Ready"

    def decide(self, user_input: str) -> str:
        """
        Basic decision logic.
        """

        text = user_input.lower().strip()

        if "hello" in text:
            return "GREETING"

        elif "time" in text:
            return "TIME"

        elif "date" in text:
            return "DATE"

        elif "bye" in text:
            return "EXIT"

        return "UNKNOWN"
    