"""
CHITT AI
Logger
"""

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
