"""
CHITT Intent Recognition Engine
"""


class Intent:

    def __init__(self):

        self.intent = "chat"

    # ==========================================
    # Detect Intent
    # ==========================================

    def detect(self, text):

        text = text.lower()

        # --------------------------------------
        # Open
        # --------------------------------------

        if any(word in text for word in [

            "open",

            "launch",

            "run",

            "start"

        ]):

            self.intent = "action"

        # --------------------------------------
        # Search
        # --------------------------------------

        elif any(word in text for word in [

            "search",

            "find",

            "lookup"

        ]):

            self.intent = "search"

        # --------------------------------------
        # Calculation
        # --------------------------------------

        elif any(word in text for word in [

            "calculate",

            "solve",

            "math"

        ]):

            self.intent = "calculation"

        # --------------------------------------
        # Question
        # --------------------------------------

        elif any(word in text for word in [

            "who",

            "what",

            "when",

            "where",

            "why",

            "how"

        ]):

            self.intent = "question"

        # --------------------------------------
        # Exit
        # --------------------------------------

        elif any(word in text for word in [

            "exit",

            "quit",

            "bye"

        ]):

            self.intent = "exit"

        else:

            self.intent = "chat"

        return self.intent

    # ==========================================
    # Get Intent
    # ==========================================

    def get(self):

        return self.intent

    # ==========================================
    # Reset
    # ==========================================

    def reset(self):

        self.intent = "chat"


if __name__ == "__main__":

    engine = Intent()

    print(engine.detect("Open Chrome"))

    print(engine.detect("Search Python"))

    print(engine.detect("What is AI"))

    print(engine.detect("Bye"))
    
