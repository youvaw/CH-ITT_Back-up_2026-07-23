"""
AetherMind File Logger
"""

import logging
from logging.handlers import RotatingFileHandler

from .config import (
    LOG_FORMAT,
    DATE_FORMAT,
    LOG_LEVEL,
    MAX_LOG_SIZE,
    BACKUP_COUNT,
)


class FileLogger:

    @staticmethod
    def create(log_file):

        handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            LOG_FORMAT,
            datefmt=DATE_FORMAT,
        )

        handler.setFormatter(formatter)

        handler.setLevel(getattr(logging, LOG_LEVEL))

        return handler
    
