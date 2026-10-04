from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse
from pathlib import Path


class Dashboard:
    def __init__(self):
        self.title = "CHITT Dashboard"
        self.version = "1.0.0"
        self.host = "127.0.0.1"
        self.port = 8000
        self.running = True

        self.app = FastAPI(
            title=self.title,
            version=self.version
        )

        self._configure()

    def _configure(self):
        try:
            self.app.mount(
                "/static",
                StaticFiles(
                    directory="src/webdashoard/static"
                ),
                name="static"
            )
        except Exception:
            pass

        @self.app.get("/", response_class=HTMLResponse)
        async def home():
            html_file = Path("src/webdashoard/templates/index.html")
            return html_file.read_text(encoding="utf-8")

    def start(self):
        self.running = True
        return {
            "success": True,
            "message": "Dashboard Started"
        }

    def stop(self):
        self.running = False
        return {
            "success": True,
            "message": "Dashboard Stopped"
        }

    def status(self):
        return {
            "running": self.running,
            "host": self.host,
            "port": self.port
        }

    def health(self):
        return {
            "module": "Dashboard",
            "status": "OK",
            "running": self.running
        }


dashboard = Dashboard()
app = dashboard.app

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


class ChatRequest(BaseModel):
    message: str


class Dashboard:
    def __init__(self):
        self.title = "CHITT Dashboard"
        self.version = "1.0.0"
        self.host = "127.0.0.1"
        self.port = 8000
        self.running = True

        self.app = FastAPI(
            title=self.title,
            version=self.version
        )

        self._configure()

    def _configure(self):

        if STATIC_DIR.exists():
            self.app.mount(
                "/static",
                StaticFiles(directory=str(STATIC_DIR)),
                name="static"
            )

        @self.app.get("/", response_class=HTMLResponse)
        async def home():
            html_file = TEMPLATES_DIR / "index.html"
            return html_file.read_text(encoding="utf-8")

        @self.app.get("/health")
        async def health():
            return self.health()

        @self.app.post("/chat")
        async def chat(request: ChatRequest):
            return {
                "success": True,
                "response": f"CHITT received: {request.message}"
            }

    def start(self):
        self.running = True

        return {
            "success": True,
            "message": "Dashboard Started"
        }

    def stop(self):
        self.running = False

        return {
            "success": True,
            "message": "Dashboard Stopped"
        }

    def status(self):
        return {
            "running": self.running,
            "host": self.host,
            "port": self.port
        }

    def health(self):
        return {
            "module": "Dashboard",
            "status": "OK",
            "running": self.running,
            "version": self.version
        }


dashboard = Dashboard()
app = dashboard.app

