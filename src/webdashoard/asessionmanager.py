"""
=========================================
CHITT - Dashboard Authentication
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import hashlib
import secrets
from datetime import datetime, timedelta


class DashboardAuthentication:

    def __init__(self):

        self.users = {}

        self.sessions = {}

        self.session_duration = 3600

    # ---------------------------------
    # Hash Password
    # ---------------------------------

    @staticmethod
    def _hash_password(password):

        return hashlib.sha256(

            password.encode("utf-8")

        ).hexdigest()

    # ---------------------------------
    # Create User
    # ---------------------------------

    def create_user(

        self,

        username,

        password

    ):

        if username in self.users:

            return False

        self.users[username] = {

            "password":

                self._hash_password(password),

            "created":

                datetime.now()

        }

        return True

    # ---------------------------------
    # Authenticate User
    # ---------------------------------

    def authenticate(

        self,

        username,

        password

    ):

        user = self.users.get(username)

        if not user:

            return False

        password_hash = self._hash_password(

            password

        )

        return secrets.compare_digest(

            user["password"],

            password_hash

        )

    # ---------------------------------
    # Create Session
    # ---------------------------------

    def create_session(self, username):

        if username not in self.users:

            return None

        token = secrets.token_urlsafe(48)

        self.sessions[token] = {

            "username": username,

            "expires":

                datetime.now()

                + timedelta(

                    seconds=self.session_duration

                )

        }

        return token

    # ---------------------------------
    # Verify Session
    # ---------------------------------

    def verify_session(self, token):

        session = self.sessions.get(token)

        if not session:

            return False

        if datetime.now() >= session["expires"]:

            del self.sessions[token]

            return False

        return True

    # ---------------------------------
    # Logout
    # ---------------------------------

    def logout(self, token):

        return self.sessions.pop(

            token,

            None

        ) is not None

    # ---------------------------------
    # Cleanup
    # ---------------------------------

    def cleanup(self):

        now = datetime.now()

        expired = [

            token

            for token, session

            in self.sessions.items()

            if now >= session["expires"]

        ]

        for token in expired:

            del self.sessions[token]

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        self.cleanup()

        return {

            "module":
                "DashboardAuthentication",

            "users":
                len(self.users),

            "sessions":
                len(self.sessions),

            "status":
                "OK"

        }


if __name__ == "__main__":

    auth = DashboardAuthentication()

    auth.create_user(

        "admin",

        "change-this-password"

    )

    if auth.authenticate(

        "admin",

        "change-this-password"

    ):

        session = auth.create_session(

            "admin"

        )

        print(

            auth.verify_session(session)

        )

    print(auth.health())
