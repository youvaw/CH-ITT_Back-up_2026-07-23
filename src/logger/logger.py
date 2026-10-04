"""
CHITT AI
Logger
"""

import importlib
import logging
from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Log Folder
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log File
LOG_FILE = LOG_DIR / "chitt.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("CHITT")
"""
AetherMind Main Logger
"""

import logging

try:
    from .config import (
        CONSOLE_LOG,
        FILE_LOG,
        SYSTEM_LOG,
    )
    from .console_handler import ConsoleLogger
except ImportError:
    from config import (
        CONSOLE_LOG,
        FILE_LOG,
        SYSTEM_LOG,
    )
    from console_handler import ConsoleLogger


def _get_file_logger_class():
    try:
        from .file_handler import FileLogger
    except ImportError:
        class FileLogger:
            @staticmethod
            def create(*args, **kwargs):
                return logging.NullHandler()

    return FileLogger


class AetherLogger:

    _logger = None

    @classmethod
    def get_logger(cls, name="AetherMind"):

        if cls._logger is not None:
            return cls._logger

        logger = logging.getLogger(name)

        logger.setLevel(logging.DEBUG)

        logger.propagate = False

        if not logger.handlers:

            if CONSOLE_LOG:
                logger.addHandler(
                    ConsoleLogger.create()
                )

            if FILE_LOG:
                file_logger_class = _get_file_logger_class()
                logger.addHandler(
                    file_logger_class.create(SYSTEM_LOG)
                )

        cls._logger = logger

        return logger
"""
AetherMind Main Logger
"""

import logging

from .config import (
    CONSOLE_LOG,
    FILE_LOG,
    SYSTEM_LOG,
)

from .console_handler import ConsoleLogger
from .file_handler import FileLogger


class AetherLogger:

    _logger = None

    @classmethod
    def get_logger(cls, name="AetherMind"):

        if cls._logger is not None:
            return cls._logger

        logger = logging.getLogger(name)

        logger.setLevel(logging.DEBUG)

        logger.propagate = False

        if not logger.handlers:

            if CONSOLE_LOG:
                logger.addHandler(
                    ConsoleLogger.create()
                )

            if FILE_LOG:
                logger.addHandler(
                    FileLogger.create(SYSTEM_LOG)
                )

        cls._logger = logger

        return logger
        
