from src.core.intent_engine import IntentEngine # pyright: ignore[reportMissingImports]
from src.core.command_registry import CommandRegistry # pyright: ignore[reportMissingImports]

intent = IntentEngine()

registry = CommandRegistry()

while True:

    command = input("You : ")

    if command.lower() == "exit":
        break

    detected = intent.detect(command)

    print("Intent :", detected)

    result = registry.execute(detected)

    if result is not None:

        print("CHITT :", result)
