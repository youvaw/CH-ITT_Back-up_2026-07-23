"""
=========================================
CHITT - API Configuration
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from pathlib import Path


class APIConfig:

    VERSION = "1.0.0"

    MODULE = "APIServer"

    ENABLED = True

    # ---------------------------------
    # Server
    # ---------------------------------

    HOST = "127.0.0.1"

    PORT = 8000

    DEBUG = False

    RELOAD = False

    WORKERS = 1

    # ---------------------------------
    # API
    # ---------------------------------

    TITLE = "CHITT API"

    DESCRIPTION = "CHITT AI Assistant API"

    API_PREFIX = "/api"

    API_VERSION = "v1"

    # ---------------------------------
    # Security
    # ---------------------------------

    API_KEY_REQUIRED = True

    TOKEN_EXPIRY = 3600

    MAX_REQUEST_SIZE = 10 * 1024 * 1024

    # ---------------------------------
    # CORS
    # ---------------------------------

    ALLOW_ORIGINS = ["*"]

    ALLOW_METHODS = ["*"]

    ALLOW_HEADERS = ["*"]

    # ---------------------------------
    # Paths
    # ---------------------------------

    ROOT = Path.cwd()

    LOGS = ROOT / "logs"

    CONFIG = ROOT / "api_server"

    TEMP = ROOT / "temp"

    # ---------------------------------
    # Initialize Directories
    # ---------------------------------

    @classmethod
    def initialize(cls):

        cls.LOGS.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.CONFIG.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.TEMP.mkdir(
            parents=True,
            exist_ok=True
        )

    # ---------------------------------
    # Information
    # ---------------------------------

    @classmethod
    def info(cls):

        return {

            "module": cls.MODULE,

            "version": cls.VERSION,

            "host": cls.HOST,

            "port": cls.PORT,

            "debug": cls.DEBUG,

            "enabled": cls.ENABLED

        }


if __name__ == "__main__":

    APIConfig.initialize()

    print(APIConfig.info())
    
