from src.core.brain_engine import BrainEngine # pyright: ignore[reportMissingImports]

API_KEY = "YOUR_GEMINI_API_KEY"

brain = BrainEngine(API_KEY)

while True:

    command = input("You : ")

    if command.lower() == "exit":
        break

    response = brain.process(command)

    print("CHITT :", response)
