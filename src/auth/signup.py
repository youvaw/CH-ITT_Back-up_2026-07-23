"""
=========================================
AetherMind - User Signup
=========================================
Project : CHITT AI Assistant
Version : 2.0.0
=========================================
"""

from src.database.manager import DatabaseManager
from src.security.password import hash_password


class Signup:

    def __init__(self):
        self.db = DatabaseManager()

    def register(
        self,
        user_id,
        name,
        password,
        nickname="",
        email="",
        phone=""
    ):
        # ---------------------------------
        # Basic Validation
        # ---------------------------------

        user_id = user_id.strip()
        name = name.strip()

        if not user_id:
            raise ValueError("User ID cannot be empty.")

        if not name:
            raise ValueError("Name cannot be empty.")

        if not password:
            raise ValueError("Password cannot be empty.")

        if len(password) < 8:
            raise ValueError(
                "Password must contain at least 8 characters."
            )

        # ---------------------------------
        # Check Existing User
        # ---------------------------------

        if self.db.query.user_exists(user_id):
            return False

        # ---------------------------------
        # Hash Password
        # ---------------------------------

        password_hash = hash_password(password)

        # ---------------------------------
        # Create User
        # ---------------------------------

        created = self.db.query.create_user(
            user_id=user_id,
            name=name,
            password_hash=password_hash,
            nickname=nickname.strip(),
            email=email.strip(),
            phone=phone.strip(),
        )

        return created

    def close(self):
        self.db.close()


if __name__ == "__main__":

    signup = Signup()

    try:
        result = signup.register(
            user_id="test_user",
            name="Test User",
            password="Chitt@123"
        )

        if result:
            print("SIGNUP: SUCCESS")
        else:
            print("SIGNUP: USER ALREADY EXISTS")

    finally:
        signup.close()
