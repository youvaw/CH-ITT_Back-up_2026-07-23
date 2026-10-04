from database.manager import DatabaseManager


def main():
    db = DatabaseManager()

    print("=" * 50)
    print("AetherMind Database Test")
    print("=" * 50)

    # Memory
    db.query.save_memory("name", "Aethira")
    memory = db.query.get_memory("name")

    print("Memory :", dict(memory) if memory else None)

    # Conversation
    db.query.save_conversation(
        "user",
        "Hello Aethira"
    )

    db.query.save_conversation(
        "assistant",
        "Hello! How can I help you?"
    )

    # Command
    db.query.save_command(
        "open chrome",
        "success"
    )

    # Error
    db.query.save_error(
        "Sample Error",
        "No Traceback"
    )

    print("Database Working Successfully ✅")

    db.close()


if __name__ == "__main__":
    main()
"""
AetherMind Complete Database Test
"""

from .manager import DatabaseManager


class DatabaseTest:

    def __init__(self):
        self.db = DatabaseManager()

    def run(self):

        print("=" * 50)
        print("AetherMind Database Test")
        print("=" * 50)

        # ----------------------------
        # User Test
        # ----------------------------
        print("\n[1] Testing Users Table")

        self.db.query.create_user(
            "USER001",
            "Avishkar",
            "Avi",
            "demo@email.com",
            "9999999999"
        )

        user = self.db.query.get_user("USER001")

        if user:
            print("✅ User Insert Successful")
            print(dict(user))
        else:
            print("❌ User Insert Failed")

        # ----------------------------
        # Memory Test
        # ----------------------------
        print("\n[2] Testing Memory Table")

        self.db.query.save_memory(
            "USER001",
            "assistant_name",
            "AetherMind"
        )

        memory = self.db.query.get_memory("USER001")

        print(f"✅ Memory Records : {len(memory)}")

        # ----------------------------
        # Conversation Test
        # ----------------------------
        print("\n[3] Testing Conversation History")

        self.db.query.save_message(
            "USER001",
            "user",
            "Hello AetherMind"
        )

        history = self.db.query.get_history("USER001")

        print(f"✅ Conversation Records : {len(history)}")

        # ----------------------------
        # Settings Test
        # ----------------------------
        print("\n[4] Testing Settings")

        self.db.query.save_setting(
            "language",
            "English"
        )

        setting = self.db.query.get_setting("language")

        print("✅ Setting Saved")
        print(setting)

        # ----------------------------
        # Skills Test
        # ----------------------------
        print("\n[5] Testing Skills")

        self.db.query.add_skill("Vision")

        skills = self.db.query.get_skills()

        print(f"✅ Skills : {len(skills)}")

        print("\n" + "=" * 50)
        print("Database Test Completed Successfully")
        print("=" * 50)

        self.db.close()


if __name__ == "__main__":
    DatabaseTest().run()
        
