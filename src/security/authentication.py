"""
=========================================
CHITT - Authentication
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import hashlib
import secrets
from datetime import datetime


class Authentication:

    def __init__(self):

        self.users = {}

        self.current_user = None

        self.session_token = None

        self.login_time = None

    # ---------------------------------
    # Hash Password
    # ---------------------------------

    def hash_password(self, password):

        return hashlib.sha256(

            password.encode("utf-8")

        ).hexdigest()

    # ---------------------------------
    # Register User
    # ---------------------------------

    def register(

        self,

        username,

        password

    ):

        if username in self.users:

            return {

                "success": False,

                "message": "User already exists."

            }

        self.users[username] = {

            "password": self.hash_password(password)

        }

        return {

            "success": True

        }

    # ---------------------------------
    # Login
    # ---------------------------------

    def login(

        self,

        username,

        password

    ):

        if username not in self.users:

            return {

                "success": False,

                "message": "User not found."

            }

        hashed = self.hash_password(password)

        if hashed != self.users[username]["password"]:

            return {

                "success": False,

                "message": "Invalid password."

            }

        self.current_user = username

        self.session_token = secrets.token_hex(32)

        self.login_time = datetime.now()

        return {

            "success": True,

            "user": username,

            "token": self.session_token

        }

    # ---------------------------------
    # Logout
    # ---------------------------------

    def logout(self):

        self.current_user = None

        self.session_token = None

        self.login_time = None

        return {

            "success": True

        }

    # ---------------------------------
    # Authenticated?
    # ---------------------------------

    def is_authenticated(self):

        return self.current_user is not None

    # ---------------------------------
    # Current User
    # ---------------------------------

    def user(self):

        return self.current_user

    # ---------------------------------
    # Session Token
    # ---------------------------------

    def token(self):

        return self.session_token

    # ---------------------------------
    # Login Time
    # ---------------------------------

    def session_info(self):

        return {

            "user": self.current_user,

            "token": self.session_token,

            "login_time": str(self.login_time)

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "Authentication",

            "status": "OK",

            "authenticated":

            self.is_authenticated()

        }


if __name__ == "__main__":

    auth = Authentication()

    auth.register(

        "admin",

        "1234"

    )

    print(

        auth.login(

            "admin",

            "1234"

        )

    )

    print(auth.health())
    
