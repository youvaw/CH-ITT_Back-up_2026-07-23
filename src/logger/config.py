"""
AetherMind Logger Configuration
"""

from pathlib import Path

# =====================================
# Log Folder
# =====================================

LOG_FOLDER = Path("logs")

LOG_FOLDER.mkdir(parents=True, exist_ok=True)

# =====================================
# Log Files
# =====================================

SYSTEM_LOG = LOG_FOLDER / "system.log"

DATABASE_LOG = LOG_FOLDER / "database.log"

MEMORY_LOG = LOG_FOLDER / "memory.log"

VOICE_LOG = LOG_FOLDER / "voice.log"

VISION_LOG = LOG_FOLDER / "vision.log"

ERROR_LOG = LOG_FOLDER / "error.log"

DEBUG_LOG = LOG_FOLDER / "debug.log"

# =====================================
# Logger Settings
# =====================================

LOG_LEVEL = "DEBUG"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

CONSOLE_LOG = True

FILE_LOG = True

MAX_LOG_SIZE = 10 * 1024 * 1024      # 10 MB

BACKUP_COUNT = 10

