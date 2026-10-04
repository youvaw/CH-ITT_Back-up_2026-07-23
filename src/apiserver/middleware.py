"""
=========================================
CHITT - API Middleware
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class APIMiddleware(BaseHTTPMiddleware):

    def __init__(

        self,

        app

    ):

        super().__init__(app)

    # ---------------------------------
    # Middleware
    # ---------------------------------

    async def dispatch(

        self,

        request: Request,

        call_next

    ):

        start = time.perf_counter()

        try:

            response = await call_next(request)

        except Exception as error:

            return JSONResponse(

                status_code=500,

                content={

                    "success": False,

                    "error": str(error)

                }

            )

        elapsed = (

            time.perf_counter()

            - start

        ) * 1000

        response.headers[

            "X-Process-Time"

        ] = f"{elapsed:.2f} ms"

        return response


# ---------------------------------
# Request Logger
# ---------------------------------

class RequestLogger:

    @staticmethod
    def log(request: Request):

        return {

            "method": request.method,

            "path": request.url.path,

            "client": (

                request.client.host

                if request.client

                else "unknown"

            )

        }


# ---------------------------------
# Simple Rate Limiter
# ---------------------------------

class RateLimiter:

    def __init__(

        self,

        limit=100

    ):

        self.limit = limit

        self.requests = {}

    def allow(

        self,

        client

    ):

        count = self.requests.get(

            client,

            0

        )

        if count >= self.limit:

            return False

        self.requests[client] = count + 1

        return True

    def reset(self):

        self.requests.clear()


# ---------------------------------
# Health
# ---------------------------------

def health():

    return {

        "module": "APIMiddleware",

        "status": "OK"

    }


if __name__ == "__main__":

    print(health())
    
