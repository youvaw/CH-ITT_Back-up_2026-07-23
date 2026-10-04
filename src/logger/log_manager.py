"""
CHITT AI
Log Manager
"""

from .logger import logger


class LogManager:

    @staticmethod
    def info(message: str):
        logger.info(message)

    @staticmethod
    def warning(message: str):
        logger.warning(message)

    @staticmethod
    def error(message: str):
        logger.error(message)

    @staticmethod
    def debug(message: str):
        logger.debug(message)

