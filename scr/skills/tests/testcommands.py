"""
CHITT v0.1
Basic Commands Test
"""

from src.skills.basic_commands import BasicCommands # type: ignore


def run():

    commands = BasicCommands()

    print("=" * 50)
    print("CHITT Basic Commands Test")
    print("=" * 50)

    print("Current Time :", commands.get_time())

    print("Current Date :", commands.get_date())

    print(commands.battery())

    print("\nOpening Notepad...")
    commands.open_notepad()

    print("Opening Calculator...")
    commands.open_calculator()

    print("Opening Explorer...")
    commands.open_explorer()

    print("Opening Google...")
    commands.open_google()

    print("\nBasic Commands Test Completed.")


if __name__ == "__main__":
    run()
