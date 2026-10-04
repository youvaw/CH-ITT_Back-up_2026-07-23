"""
=========================================
CHITT - Encryption
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import base64
from cryptography.fernet import Fernet


class Encryption:

    def __init__(self, key=None):

        if key is None:

            self.key = Fernet.generate_key()

        else:

            if isinstance(key, str):

                key = key.encode("utf-8")

            self.key = key

        self.cipher = Fernet(self.key)

    # ---------------------------------
    # Generate Key
    # ---------------------------------

    @staticmethod
    def generate_key():

        return Fernet.generate_key()

    # ---------------------------------
    # Export Key
    # ---------------------------------

    def export_key(self):

        return self.key.decode("utf-8")

    # ---------------------------------
    # Import Key
    # ---------------------------------

    def import_key(self, key):

        if isinstance(key, str):

            key = key.encode("utf-8")

        self.key = key

        self.cipher = Fernet(self.key)

        return True

    # ---------------------------------
    # Encrypt
    # ---------------------------------

    def encrypt(self, data):

        if isinstance(data, str):

            data = data.encode("utf-8")

        encrypted = self.cipher.encrypt(data)

        return encrypted.decode("utf-8")

    # ---------------------------------
    # Decrypt
    # ---------------------------------

    def decrypt(self, encrypted):

        if isinstance(encrypted, str):

            encrypted = encrypted.encode("utf-8")

        decrypted = self.cipher.decrypt(encrypted)

        return decrypted.decode("utf-8")

    # ---------------------------------
    # Encode Base64
    # ---------------------------------

    def encode(self, text):

        return base64.b64encode(

            text.encode("utf-8")

        ).decode("utf-8")

    # ---------------------------------
    # Decode Base64
    # ---------------------------------

    def decode(self, text):

        return base64.b64decode(

            text.encode("utf-8")

        ).decode("utf-8")

    # ---------------------------------
    # Verify Encryption
    # ---------------------------------

    def verify(self, plain, encrypted):

        try:

            return self.decrypt(encrypted) == plain

        except Exception:

            return False

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "Encryption",

            "algorithm": "Fernet (AES-128)",

            "status": "OK"

        }


if __name__ == "__main__":

    enc = Encryption()

    secret = enc.encrypt("Hello CHITT")

    print("Encrypted :", secret)

    print("Decrypted :", enc.decrypt(secret))

    print(enc.health())
    
