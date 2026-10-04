"""
=========================================
CHITT - User Memory
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os


class UserMemory:

    def __init__(self):

        self.user = {}

        self.file_path = os.path.join(
            os.path.dirname(__file__),
            "user_profile.json"
        )

        self.load()

    # ---------------------------------
    # Save User Data
    # ---------------------------------

    def save(self, key, value):

        self.user[key] = value

        self.save_file()

    # ---------------------------------
    # Load User Data
    # ---------------------------------

    def load(self, key=None):

        if key is None:

            if not os.path.exists(self.file_path):

                self.user = {}

                return

            try:

                with open(
                    self.file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.user = json.load(file)

            except Exception:

                self.user = {}

            return

        return self.user.get(key)

    # ---------------------------------
    # Update User Data
    # ---------------------------------

    def update(self, key, value):

        self.user[key] = value

        self.save_file()

    # ---------------------------------
    # Delete User Data
    # ---------------------------------

    def delete(self, key):

        if key in self.user:

            del self.user[key]

            self.save_file()

            return True

        return False

    # ---------------------------------
    # Exists
    # ---------------------------------

    def exists(self, key):

        return key in self.user

    # ---------------------------------
    # Get All
    # ---------------------------------

    def get_all(self):

        return self.user

    # ---------------------------------
    # Count
    # ---------------------------------

    def count(self):

        return len(self.user)

    # ---------------------------------
    # Clear
    # ---------------------------------

    def clear(self):

        self.user.clear()

        self.save_file()

    # ---------------------------------
    # Save File
    # ---------------------------------

    def save_file(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.user,
                file,
                indent=4
            )

    # ---------------------------------
    # Show User Profile
    # ---------------------------------

    def show(self):

        print("\n===== USER PROFILE =====\n")

        if not self.user:

            print("Profile Empty.")

            return

        for key, value in self.user.items():

            print(f"{key} : {value}")


if __name__ == "__main__":

    profile = UserMemory()

    profile.save("name", "AVISHKAR")

    profile.save("language", "English")

    profile.save("city", "Mumbai")

    profile.show()

    print("\nName :", profile.load("name"))

    print("Total :", profile.count())
    
