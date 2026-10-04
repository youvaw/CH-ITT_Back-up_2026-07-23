class CommandRouter: # pyright: ignore[reportRedeclaration]

    def __init__(self, core):
        self.core = core

    def execute(self, command):

        command = command.lower().strip()

        if command == "hello":
            return self.core.run_plugin("hello")

        elif command.startswith("save my name"):
            name = command.replace("save my name", "").strip()

            self.core.save_memory("owner", name)

            return f"Name '{name}' saved."

        elif command == "show memory":
            return self.core.memory.show_all()

        elif command == "plugins":
            return self.core.show_plugins()

        else:
            return "Sorry, I don't understand this command."
        
class CommandRouter:

    def __init__(self, core):
        self.core = core

    def execute(self, command):

        command = command.strip()

        if not command:
            return "Please enter a command."

        command_lower = command.lower()

        if command_lower == "hello":
            return self.core.run_plugin("hello")

        elif command_lower.startswith("save my name"):
            name = command[len("save my name"):].strip()

            if not name:
                return "Please provide your name."

            self.core.save_memory("owner", name)
            return f"Name '{name}' saved successfully."

        elif command_lower == "show memory":
            return self.core.memory.show_all()

        elif command_lower == "plugins":
            return self.core.show_plugins()

        else:
            return f"Unknown command: {command}"
                
