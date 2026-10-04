import hashlib
import json
import os

class AuthSystem:
    def __init__(self, db_path="users.json"):
        self.db_path = db_path

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password) -> bool:
        if not os.path.exists(self.db_path):
            return False

        with open(self.db_path, "r") as f:
            users = json.load(f)

        hashed_pwd = self._hash_password(password)
        if username in users and users[username] == hashed_pwd:
            return True
        return False
