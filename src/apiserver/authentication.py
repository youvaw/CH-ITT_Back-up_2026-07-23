"""
=========================================
CHITT - API Authentication
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import secrets
from datetime import datetime, timedelta


class APIAuthentication:

    def __init__(self):

        self.api_keys = {}

        self.tokens = {}

        self.token_expiry = 3600

    # ---------------------------------
    # Create API Key
    # ---------------------------------

    def create_api_key(self, user):

        key = secrets.token_hex(32)

        self.api_keys[key] = {

            "user": user,

            "created": datetime.now()

        }

        return key

    # ---------------------------------
    # Verify API Key
    # ---------------------------------

    def verify_api_key(self, key):

        return key in self.api_keys

    # ---------------------------------
    # Create Access Token
    # ---------------------------------

    def create_token(self, user):

        token = secrets.token_urlsafe(48)

        self.tokens[token] = {

            "user": user,

            "expires": datetime.now() +

                       timedelta(

                           seconds=self.token_expiry

                       )

        }

        return token

    # ---------------------------------
    # Verify Token
    # ---------------------------------

    def verify_token(self, token):

        if token not in self.tokens:

            return False

        expiry = self.tokens[token]["expires"]

        return datetime.now() < expiry

    # ---------------------------------
    # Revoke Token
    # ---------------------------------

    def revoke_token(self, token):

        if token in self.tokens:

            del self.tokens[token]

            return True

        return False

    # ---------------------------------
    # Cleanup Expired Tokens
    # ---------------------------------

    def cleanup(self):

        expired = [

            token

            for token, data

            in self.tokens.items()

            if datetime.now() >= data["expires"]

        ]

        for token in expired:

            del self.tokens[token]

    # ---------------------------------
    # Active Tokens
    # ---------------------------------

    def active_tokens(self):

        self.cleanup()

        return len(self.tokens)

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        self.cleanup()

        return {

            "module": "APIAuthentication",

            "api_keys": len(self.api_keys),

            "tokens": len(self.tokens),

            "status": "OK"

        }


if __name__ == "__main__":

    auth = APIAuthentication()

    api_key = auth.create_api_key("admin")

    token = auth.create_token("admin")

    print(auth.verify_api_key(api_key))

    print(auth.verify_token(token))

    print(auth.health())
