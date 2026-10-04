class ConversationEngine:

    def __init__(self):
        self.history = []

    def add(self, role, message):
        self.history.append({
            "role": role,
            "message": message
        })

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()

    def last_message(self):
        if not self.history:
            return None

        return self.history[-1]
    
