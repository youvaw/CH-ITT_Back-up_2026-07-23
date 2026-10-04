class IntentAnalyzer:

    def __init__(self):
        self.intents = {
            "greeting": ["hello", "hi", "hey"],
            "save_name": ["my name is", "i am"],
            "show_memory": ["show memory", "memory"],
            "plugins": ["plugins", "skills"],
            "exit": ["bye", "goodbye", "exit"]
        }

    def analyze(self, text):

        text = text.lower().strip()

        for intent, keywords in self.intents.items():
            for keyword in keywords:

                if keyword in text:
                    return intent

        return "unknown"
    
