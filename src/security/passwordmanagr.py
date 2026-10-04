"""
=========================================
CHITT - Password Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import bcrypt
import secrets
import string


class PasswordManager:

    def __init__(self):

        self.minimum_length = 8

    # ---------------------------------
    # Hash Password
    # ---------------------------------

    def hash(self, password):

        password = password.encode("utf-8")

        hashed = bcrypt.hashpw(

            password,

            bcrypt.gensalt()

        )

        return hashed.decode("utf-8")

    # ---------------------------------
    # Verify Password
    # ---------------------------------

    def verify(

        self,

        password,

        hashed

    ):

        return bcrypt.checkpw(

            password.encode("utf-8"),

            hashed.encode("utf-8")

        )

    # ---------------------------------
    # Generate Password
    # ---------------------------------

    def generate(

        self,

        length=16

    ):

        characters = (

            string.ascii_letters +

            string.digits +

            string.punctuation

        )

        return "".join(

            secrets.choice(characters)

            for _ in range(length)

        )

    # ---------------------------------
    # Password Strength
    # ---------------------------------

    def strength(self, password):

        score = 0

        if len(password) >= self.minimum_length:
            score += 1

        if any(c.islower() for c in password):
            score += 1

        if any(c.isupper() for c in password):
            score += 1

        if any(c.isdigit() for c in password):
            score += 1

        if any(c in string.punctuation for c in password):
            score += 1

        if score <= 2:
            return "Weak"

        elif score == 3:
            return "Medium"

        elif score == 4:
            return "Strong"

        return "Very Strong"

    # ---------------------------------
    # Password Policy
    # ---------------------------------

    def valid(self, password):

        return (

            len(password) >= self.minimum_length

            and any(c.islower() for c in password)

            and any(c.isupper() for c in password)

            and any(c.isdigit() for c in password)

        )

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "PasswordManager",

            "algorithm": "bcrypt",

            "minimum_length": self.minimum_length,

            "status": "OK"

        }


if __name__ == "__main__":

    manager = PasswordManager()

    password = manager.generate()

    hashed = manager.hash(password)

    print("Password :", password)

    print("Hash :", hashed)

    print("Verify :", manager.verify(password, hashed))

    print("Strength :", manager.strength(password))

    print(manager.health())
    
