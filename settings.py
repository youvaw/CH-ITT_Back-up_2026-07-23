"""
CHITT AI
Application Settings
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppSettings:
    """Application Configuration"""

    APP_NAME: str = "CHITT AI"
    VERSION: str = "0.1.0"

    AUTHOR: str = "Your Name"

    DEBUG: bool = True

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    LOG_DIR: Path = BASE_DIR / "logs"

    DATA_DIR: Path = BASE_DIR / "data"

    PLUGIN_DIR: Path = BASE_DIR / "plugins"


settings = AppSettings()

