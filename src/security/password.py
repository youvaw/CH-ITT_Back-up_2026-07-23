"""
=========================================
AetherMind - Password Security
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 2.0.0
=========================================
"""

import hashlib
import hmac
import secrets


# -----------------------------------------
# Security Configuration
# -----------------------------------------

SALT_LENGTH = 32
ITERATIONS = 600_000
HASH_NAME = "sha256"


# -----------------------------------------
# Hash Password
# -----------------------------------------

def hash_password(password: str) -> str:
    """
    Create a secure salted password hash.

    Stored format:
        salt$hash
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        raise ValueError("Password cannot be empty.")

    salt = secrets.token_bytes(SALT_LENGTH)

    password_hash = hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )

    return (
        salt.hex()
        + "$"
        + password_hash.hex()
    )


# -----------------------------------------
# Verify Password
# -----------------------------------------

def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against the stored hash.
    """

    if not isinstance(password, str):
        return False

    if not isinstance(stored_hash, str):
        return False

    try:
        salt_hex, hash_hex = stored_hash.split("$", 1)

        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            HASH_NAME,
            password.encode("utf-8"),
            salt,
            ITERATIONS,
        )

        return hmac.compare_digest(
            actual_hash,
            expected_hash,
        )

    except (ValueError, TypeError):
        return False
