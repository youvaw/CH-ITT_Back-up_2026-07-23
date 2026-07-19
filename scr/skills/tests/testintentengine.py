from src.core.intent_engine import IntentEngine # type: ignore

engine = IntentEngine()

commands = [

    "Open Google",

    "Open YouTube",

    "Open Notepad",

    "Battery Percentage",

    "Current Time",

    "Today's Date",

    "Hello CHITT"

]

for cmd in commands:

    print(cmd, "------>", engine.detect(cmd))
