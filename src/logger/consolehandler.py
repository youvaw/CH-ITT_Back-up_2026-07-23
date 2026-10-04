"""
AetherMind Console Logger
"""

import logging

from .config import (
    LOG_FORMAT,
    DATE_FORMAT,
    LOG_LEVEL,
)


class ConsoleLogger:

    @staticmethod
    def create():

        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            LOG_FORMAT,
            datefmt=DATE_FORMAT,
        )

        handler.setFormatter(formatter)

        handler.setLevel(getattr(logging, LOG_LEVEL))

        return handler
    
