"""
=========================================
CHITT - WebSocket Server
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect


class WebSocketServer:

    def __init__(self):

        self.router = APIRouter()

        self.connections = []

        self._register_routes()

    # ---------------------------------
    # Register Routes
    # ---------------------------------

    def _register_routes(self):

        @self.router.websocket("/ws")
        async def websocket_endpoint(
            websocket: WebSocket
        ):

            await self.connect(websocket)

            try:

                while True:

                    message = await websocket.receive_text()

                    await self.send(

                        websocket,

                        f"Echo: {message}"

                    )

            except WebSocketDisconnect:

                self.disconnect(websocket)

    # ---------------------------------
    # Connect
    # ---------------------------------

    async def connect(self, websocket):

        await websocket.accept()

        self.connections.append(websocket)

    # ---------------------------------
    # Disconnect
    # ---------------------------------

    def disconnect(self, websocket):

        if websocket in self.connections:

            self.connections.remove(websocket)

    # ---------------------------------
    # Send
    # ---------------------------------

    async def send(

        self,

        websocket,

        message

    ):

        await websocket.send_text(message)

    # ---------------------------------
    # Broadcast
    # ---------------------------------

    async def broadcast(self, message):

        disconnected = []

        for connection in self.connections:

            try:

                await connection.send_text(message)

            except Exception:

                disconnected.append(connection)

        for connection in disconnected:

            self.disconnect(connection)

    # ---------------------------------
    # Active Connections
    # ---------------------------------

    def active(self):

        return len(self.connections)

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "WebSocketServer",

            "connections": self.active(),

            "status": "OK"

        }


websocket_server = WebSocketServer()

router = websocket_server.router


if __name__ == "__main__":

    print(websocket_server.health())
    
