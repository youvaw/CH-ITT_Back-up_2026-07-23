import google.generativeai as genai 


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

"""
CHITT Reasoning Engine
Handles analysis and logical thinking
"""


class ReasoningEngine:

    def __init__(self):

        self.reasoning_history = []

    # ==========================================
    # Process User Input
    # ==========================================

    def process(self, user_input):

        result = {

            "input": user_input,

            "intent": self.detect_intent(user_input),

            "complexity": self.detect_complexity(user_input),

            "requires_tools": self.requires_tool(user_input)

        }

        self.reasoning_history.append(result)

        return result

    # ==========================================
    # Detect Intent
    # ==========================================

    def detect_intent(self, text):

        text = text.lower()

        if any(word in text for word in [
            "open",
            "run",
            "start"
        ]):
            return "ACTION"

        elif any(word in text for word in [
            "calculate",
            "solve",
            "math"
        ]):
            return "CALCULATION"

        elif any(word in text for word in [
            "search",
            "find",
            "look"
        ]):
            return "SEARCH"

        elif any(word in text for word in [
            "who",
            "what",
            "why",
            "when",
            "how"
        ]):
            return "QUESTION"

        return "CHAT"

    # ==========================================
    # Complexity
    # ==========================================

    def detect_complexity(self, text):

        words = len(text.split())

        if words < 5:
            return "LOW"

        elif words < 15:
            return "MEDIUM"

        return "HIGH"

    # ==========================================
    # Tool Requirement
    # ==========================================

    def requires_tool(self, text):

        text = text.lower()

        keywords = [

            "open",

            "file",

            "folder",

            "browser",

            "youtube",

            "music",

            "camera",

            "terminal"

        ]

        return any(k in text for k in keywords)

    # ==========================================
    # History
    # ==========================================

    def history(self):

        return self.reasoning_history


if __name__ == "__main__":

    engine = ReasoningEngine()

    result = engine.process(

        "Open YouTube"

    )

    print(result)

import google.generativeai as genai

# अपनी API Key यहाँ डालें
genai.configure(api_key="YOUR_API_KEY")

class ReasoningEngine:
    def __init__(self):
        self.status = "Ready"
        # Gemini model initialize करें
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def reason(self, decision: str) -> str:
        if decision == "GREETING":
            return "Hello! Welcome to CHITT AI."
        elif decision == "TIME":
            return "The user wants to know the current time."
        elif decision == "DATE":
            return "The user wants today's date."
        elif decision == "EXIT":
            return "The user wants to close CHITT."
        else:
            # Fallback logic: Gemini API call
            response = self.model.generate_content(decision)
            return response.text

from src.core.startup import start
# ReasoningEngine को इंपोर्ट करें
from reasoningengine import ReasoningEngine

if __name__ == "__main__":
    # Startup शुरू करें
    start()
    
    # Reasoning Engine शुरू करें
    engine = ReasoningEngine()
    
    # टेस्ट करने के लिए Gemini से कोई सवाल पूछें
    user_input = "Tell me a short motivational quote"
    response = engine.reason(user_input)
    
    print("\n--- CHITT Response ---")
    print(response)
                
