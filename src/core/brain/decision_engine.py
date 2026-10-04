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
"""
CHITT Decision Engine
Chooses the best action for a task
"""


class DecisionEngine:

    def __init__(self):

        self.history = []

    # ==========================================
    # Make Decision
    # ==========================================

    def make(self, plan):

        intent = plan["intent"]

        if intent == "ACTION":

            decision = self.action()

        elif intent == "SEARCH":

            decision = self.search()

        elif intent == "CALCULATION":

            decision = self.math()

        elif intent == "QUESTION":

            decision = self.question()

        else:

            decision = self.chat()

        self.history.append(decision)

        return decision

    # ==========================================
    # Decisions
    # ==========================================

    def action(self):

        return {

            "tool": "ToolManager",

            "model": None,

            "execute": True

        }

    def search(self):

        return {

            "tool": "Search",

            "model": "Gemini",

            "execute": True

        }

    def math(self):

        return {

            "tool": None,

            "model": "Gemini",

            "execute": False

        }

    def question(self):

        return {

            "tool": None,

            "model": "Gemini",

            "execute": False

        }

    def chat(self):

        return {

            "tool": None,

            "model": "Gemini",

            "execute": False

        }

    # ==========================================
    # History
    # ==========================================

    def get_history(self):

        return self.history

    # ==========================================
    # Last Decision
    # ==========================================

    def last(self):

        if self.history:

            return self.history[-1]

        return None


if __name__ == "__main__":

    engine = DecisionEngine()

    plan = {

        "intent": "ACTION"

    }

    print(engine.make(plan))
        
