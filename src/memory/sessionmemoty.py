"""
=========================================
CHITT - Session Memory
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class SessionMemory:

    def __init__(self):

        self.session = {}

        self.start_time = None

    # ---------------------------------
    # Save Session Data
    # ---------------------------------

    def save(self, key, value):

        self.session[key] = value

    # ---------------------------------
    # Load Session Data
    # ---------------------------------

    def load(self, key):

        return self.session.get(key)

    # ---------------------------------
    # Update Session Data
    # ---------------------------------

    def update(self, key, value):

        self.session[key] = value

    # ---------------------------------
    # Delete Session Data
    # ---------------------------------

    def delete(self, key):

        if key in self.session:

            del self.session[key]

            return True

        return False

    # ---------------------------------
    # Check Session Data
    # ---------------------------------

    def exists(self, key):

        return key in self.session

    # ---------------------------------
    # Get All Session Data
    # ---------------------------------

    def get_all(self):

        return self.session

    # ---------------------------------
    # Session Count
    # ---------------------------------

    def count(self):

        return len(self.session)

    # ---------------------------------
    # Clear Session
    # ---------------------------------

    def clear(self):

        self.session.clear()

    # ---------------------------------
    # Show Session
    # ---------------------------------

    def show(self):

        print("\n===== SESSION MEMORY =====\n")

        if not self.session:

            print("Session Empty.")

            return

        for key, value in self.session.items():

            print(f"{key} : {value}")


if __name__ == "__main__":

    session = SessionMemory()

    session.save("current_user", "AVISHKAR")

    session.save("current_command", "Open YouTube")

    session.show()

    print("\nCount :", session.count())

    print("\nCurrent User :", session.load("current_user"))
    
