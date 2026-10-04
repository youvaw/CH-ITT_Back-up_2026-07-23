class TaskManager:

    def __init__(self, brain):
        self.brain = brain

    def execute(self, intent, data=None):

        if intent == "greeting":
            return self.brain.router.execute("hello")

        elif intent == "save_name":
            return self.brain.router.execute(f"save my name {data}")

        elif intent == "show_memory":
            return self.brain.router.execute("show memory")

        elif intent == "plugins":
            return self.brain.router.execute("plugins")

        else:
            return f"Task '{intent}' is not implemented."
        
