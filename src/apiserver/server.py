"""
=========================================
CHITT - API Server
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from fastapi import FastAPI
import uvicorn


class APIServer:

    def __init__(self):

        self.host = "127.0.0.1"

        self.port = 8000

        self.running = False

        self.app = FastAPI(

            title="CHITT API",

            version="1.0.0",

            description="CHITT AI Assistant API"

        )

        self._register_default_routes()

    # ---------------------------------
    # Default Routes
    # ---------------------------------

    def _register_default_routes(self):

        @self.app.get("/")

        async def home():

            return {

                "name": "CHITT API",

                "version": "1.0.0",

                "status": "running"

            }

        @self.app.get("/health")

        async def health():

            return self.health()

    # ---------------------------------
    # Start Server
    # ---------------------------------

    def start(

        self,

        host=None,

        port=None

    ):

        if host:

            self.host = host

        if port:

            self.port = port

        self.running = True

        uvicorn.run(

            self.app,

            host=self.host,

            port=self.port

        )

    # ---------------------------------
    # Stop Server
    # ---------------------------------

    def stop(self):

        self.running = False

        return {

            "success": True,

            "message": "Server stopped"

        }

    # ---------------------------------
    # Add Route
    # ---------------------------------

    def add_route(

        self,

        path,

        endpoint,

        methods=["GET"]

    ):

        self.app.add_api_route(

            path,

            endpoint,

            methods=methods

        )

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "APIServer",

            "running": self.running,

            "host": self.host,

            "port": self.port,

            "status": "OK"

        }


if __name__ == "__main__":

    server = APIServer()

    server.start()
    
