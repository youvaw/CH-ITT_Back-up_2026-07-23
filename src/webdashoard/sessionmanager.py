"""
=========================================
CHITT - Dashboard Session Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import secrets
from datetime import datetime, timedelta


class SessionManager:

    def __init__(self, session_duration=3600):

        self.sessions = {}

        self.session_duration = session_duration

    # ---------------------------------
    # Create Session
    # ---------------------------------

    def create(self, username):

        session_id = secrets.token_urlsafe(48)

        self.sessions[session_id] = {

            "username": username,

            "created":

                datetime.now(),

            "expires":

                datetime.now()

                + timedelta(

                    seconds=self.session_duration

                )

        }

        return session_id

    # ---------------------------------
    # Get Session
    # ---------------------------------

    def get(self, session_id):

        self.cleanup()

        return self.sessions.get(

            session_id

        )

    # ---------------------------------
    # Verify Session
    # ---------------------------------

    def verify(self, session_id):

        return self.get(session_id) is not None

    # ---------------------------------
    # Username
    # ---------------------------------

    def username(self, session_id):

        session = self.get(session_id)

        if not session:

            return None

        return session["username"]

    # ---------------------------------
    # Refresh Session
    # ---------------------------------

    def refresh(self, session_id):

        session = self.get(session_id)

        if not session:

            return False

        session["expires"] = (

            datetime.now()

            + timedelta(

                seconds=self.session_duration

            )

        )

        return True

    # ---------------------------------
    # Destroy Session
    # ---------------------------------

    def destroy(self, session_id):

        return self.sessions.pop(

            session_id,

            None

        ) is not None

    # ---------------------------------
    # Destroy User Sessions
    # ---------------------------------

    def destroy_user(self, username):

        sessions = [

            session_id

            for session_id, session

            in self.sessions.items()

            if session["username"] == username

        ]

        for session_id in sessions:

            del self.sessions[session_id]

        return len(sessions)

    # ---------------------------------
    # Cleanup Expired Sessions
    # ---------------------------------

    def cleanup(self):

        now = datetime.now()

        expired = [

            session_id

            for session_id, session

            in self.sessions.items()

            if now >= session["expires"]

        ]

        for session_id in expired:

            del self.sessions[session_id]

    # ---------------------------------
    # Active Sessions
    # ---------------------------------

    def active_count(self):

        self.cleanup()

        return len(self.sessions)

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        self.cleanup()

        return {

            "module":
                "SessionManager",

            "active_sessions":
                len(self.sessions),

            "status":
                "OK"

        }


if __name__ == "__main__":

    manager = SessionManager()

    session = manager.create("admin")

    print(

        "Session:",

        session

    )

    print(

        "Valid:",

        manager.verify(session)

    )

    print(

        "User:",

        manager.username(session)

    )

    print(manager.health())
    
