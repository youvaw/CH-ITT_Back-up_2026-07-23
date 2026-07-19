"""
CHITT AI
Environment Configuration
"""

from enum import Enum


class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


CURRENT_ENVIRONMENT = Environment.DEVELOPMENT


def is_development() -> bool:
    return CURRENT_ENVIRONMENT == Environment.DEVELOPMENT


def is_testing() -> bool:
    return CURRENT_ENVIRONMENT == Environment.TESTING


def is_production() -> bool:
    return CURRENT_ENVIRONMENT == Environment.PRODUCTION
