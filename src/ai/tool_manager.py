"""
CHITT Tool Manager
"""


class ToolManager:

    def __init__(self):

        self.tools = {}

    def register(self, name, function):

        self.tools[name] = function

    def execute(self, name, *args, **kwargs):

        if name not in self.tools:
            return f"{name} not found."

        return self.tools[name](*args, **kwargs)
    
