"""
CHITT AI
Planning Engine
"""


class PlanningEngine:
    """
    Responsible for creating execution plans.
    """

    def __init__(self):
        self.status = "Ready"

    def create_plan(self, goal: str) -> list[str]:
        """
        Create a simple execution plan.
        """

        return [
            f"Understand goal: {goal}",
            "Collect required information",
            "Generate possible actions",
            "Select best action",
            "Execute action",
            "Evaluate result",
        ]
"""
CHITT Planning Engine
Creates execution plans for tasks
"""


class PlanningEngine:

    def __init__(self):

        self.plan_history = []

    # ==========================================
    # Create Plan
    # ==========================================

    def create(self, reasoning):

        intent = reasoning["intent"]

        if intent == "ACTION":

            steps = self.action_plan(reasoning)

        elif intent == "SEARCH":

            steps = self.search_plan(reasoning)

        elif intent == "CALCULATION":

            steps = self.math_plan(reasoning)

        elif intent == "QUESTION":

            steps = self.question_plan(reasoning)

        else:

            steps = self.chat_plan(reasoning)

        plan = {

            "intent": intent,

            "steps": steps,

            "completed": False

        }

        self.plan_history.append(plan)

        return plan

    # ==========================================
    # Action Plan
    # ==========================================

    def action_plan(self, reasoning):

        return [

            "Understand Command",

            "Check Permissions",

            "Select Tool",

            "Execute Action",

            "Verify Result"

        ]

    # ==========================================
    # Search Plan
    # ==========================================

    def search_plan(self, reasoning):

        return [

            "Analyze Query",

            "Search Information",

            "Filter Results",

            "Generate Response"

        ]

    # ==========================================
    # Math Plan
    # ==========================================

    def math_plan(self, reasoning):

        return [

            "Parse Expression",

            "Calculate",

            "Verify Answer",

            "Return Result"

        ]

    # ==========================================
    # Question Plan
    # ==========================================

    def question_plan(self, reasoning):

        return [

            "Understand Question",

            "Collect Knowledge",

            "Generate Explanation",

            "Return Answer"

        ]

    # ==========================================
    # Chat Plan
    # ==========================================

    def chat_plan(self, reasoning):

        return [

            "Understand User",

            "Generate Friendly Reply"

        ]

    # ==========================================
    # Get History
    # ==========================================

    def history(self):

        return self.plan_history


if __name__ == "__main__":

    engine = PlanningEngine()

    reasoning = {

        "intent": "ACTION"

    }

    plan = engine.create(reasoning)

    print(plan)
        
