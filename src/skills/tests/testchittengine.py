from src.core.chitt_engine import CHITTEngine # type: ignore

engine = CHITTEngine()

print("=" * 50)
print("CHITT v0.1")
print("=" * 50)

while True:

    command = input("You : ")

    if command.lower() == "exit":
        break

    response = engine.execute(command)

    if response is not None:

        print("CHITT :", response)

