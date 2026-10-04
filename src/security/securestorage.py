"""
=========================================
CHITT - Secure Storage
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
from pathlib import Path

from security.encryption import Encryption


class SecureStorage:

    def __init__(self, storage_file="security/secure_storage.json"):

        self.storage_file = Path(storage_file)

        self.storage_file.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        self.encryption = Encryption()

        self.data = {}

        self.load()

    # ---------------------------------
    # Load Storage
    # ---------------------------------

    def load(self):

        if self.storage_file.exists():

            try:

                with open(

                    self.storage_file,

                    "r",

                    encoding="utf-8"

                ) as file:

                    self.data = json.load(file)

            except Exception:

                self.data = {}

    # ---------------------------------
    # Save Storage
    # ---------------------------------

    def save_storage(self):

        with open(

            self.storage_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.data,

                file,

                indent=4

            )

    # ---------------------------------
    # Save Secret
    # ---------------------------------

    def save(self, key, value):

        encrypted = self.encryption.encrypt(str(value))

        self.data[key] = encrypted

        self.save_storage()

        return {

            "success": True,

            "key": key

        }

    # ---------------------------------
    # Load Secret
    # ---------------------------------

    def load_secret(self, key):

        if key not in self.data:

            return None

        try:

            return self.encryption.decrypt(

                self.data[key]

            )

        except Exception:

            return None

    # ---------------------------------
    # Delete Secret
    # ---------------------------------

    def delete(self, key):

        if key in self.data:

            del self.data[key]

            self.save_storage()

            return True

        return False

    # ---------------------------------
    # Exists
    # ---------------------------------

    def exists(self, key):

        return key in self.data

    # ---------------------------------
    # List Keys
    # ---------------------------------

    def keys(self):

        return list(self.data.keys())

    # ---------------------------------
    # Clear Storage
    # ---------------------------------

    def clear(self):

        self.data.clear()

        self.save_storage()

    # ---------------------------------
    # Export (Encrypted)
    # ---------------------------------

    def export(self):

        return self.data

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "SecureStorage",

            "entries": len(self.data),

            "status": "OK"

        }


if __name__ == "__main__":

    storage = SecureStorage()

    storage.save(

        "api_key",

        "123456789"

    )

    print(

        storage.load_secret("api_key")

    )

    print(storage.health())
    
