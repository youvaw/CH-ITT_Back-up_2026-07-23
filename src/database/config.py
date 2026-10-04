"""
=========================================
AetherMind - Database Configuration
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.1.0
=========================================
"""

from pathlib import Path


# ==================================================
# PROJECT PATH
# ==================================================

# src/database/config.py
# parent      -> database
# parent.parent -> src
# parent.parent.parent -> project root

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ==================================================
# DATABASE
# ==================================================

DATA_DIR = PROJECT_ROOT / "data"

DATABASE_NAME = "AetherMind.db"

DATABASE_PATH = DATA_DIR / DATABASE_NAME


# ==================================================
# BACKUP
# ==================================================

BACKUP_DIR = DATA_DIR / "backups"

MAX_BACKUPS = 20

AUTO_BACKUP = True


# ==================================================
# SQLITE
# ==================================================

SQLITE_TIMEOUT = 30

CHECK_SAME_THREAD = False

ENABLE_FOREIGN_KEYS = True

ENABLE_WAL_MODE = True

ENABLE_JOURNAL = True

JOURNAL_MODE = "WAL"

SYNCHRONOUS = "NORMAL"

CACHE_SIZE = -64000

TEMP_STORE = "MEMORY"

PAGE_SIZE = 4096


# ==================================================
# PERFORMANCE
# ==================================================

AUTO_VACUUM = True

AUTO_COMMIT = True

FETCH_SIZE = 100


# ==================================================
# DEBUG
# ==================================================

DEBUG_DATABASE = True

LOG_SQL = False


# ==================================================
# DATABASE VERSION
# ==================================================

DATABASE_VERSION = "1.0.0"


# ==================================================
# CREATE REQUIRED DIRECTORIES
# ==================================================

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True
)
