"""
=========================================
CHITT - Request Handler
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from datetime import datetime


class RequestHandler:

    def __init__(self):

        self.request_count = 0

    # ---------------------------------
    # Handle Request
    # ---------------------------------

    def handle(

        self,

        endpoint,

        payload=None

    ):

        self.request_count += 1

        return {

            "success": True,

            "endpoint": endpoint,

            "payload": payload,

            "timestamp": str(

                datetime.now()

            )

        }

    # ---------------------------------
    # Validate Request
    # ---------------------------------

    def validate(

        self,

        payload

    ):

        if payload is None:

            return False

        return True

    # ---------------------------------
    # Parse Request
    # ---------------------------------

    def parse(

        self,

        payload

    ):

        if isinstance(payload, dict):

            return payload

        return {

            "data": payload

        }

    # ---------------------------------
    # Request Statistics
    # ---------------------------------

    def statistics(self):

        return {

            "total_requests":

                self.request_count

        }

    # ---------------------------------
    # Reset Counter
    # ---------------------------------

    def reset(self):

        self.request_count = 0

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "RequestHandler",

            "requests":

                self.request_count,

            "status": "OK"

        }


if __name__ == "__main__":

    handler = RequestHandler()

    print(

        handler.handle(

            "/chat",

            {

                "message": "Hello"

            }

        )

    )

    print(handler.health())
    
