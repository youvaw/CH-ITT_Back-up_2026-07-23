"""
CHITT System Configuration
"""

from pathlib import Path


# =====================================================
# PROJECT
# =====================================================

PROJECT_NAME = "CHITT"

VERSION = "2.0.0"

AUTHOR = "Avishkar"


# =====================================================
# ROOT
# =====================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

LOG_DIR = ROOT_DIR / "logs"

CACHE_DIR = ROOT_DIR / "cache"

PLUGIN_DIR = ROOT_DIR / "plugins"

TEMP_DIR = ROOT_DIR / "temp"


# =====================================================
# CREATE DIRECTORIES
# =====================================================

for directory in [

    DATA_DIR,

    LOG_DIR,

    CACHE_DIR,

    PLUGIN_DIR,

    TEMP_DIR

]:

    directory.mkdir(

        parents=True,

        exist_ok=True

    )


# =====================================================
# SYSTEM SETTINGS
# =====================================================

DEBUG = True

AUTO_SAVE = True

AUTO_BACKUP = True

SAFE_MODE = False


# =====================================================
# VOICE
# =====================================================

VOICE_ENABLED = True

DEFAULT_VOICE = "Female"

DEFAULT_LANGUAGE = "English"


# =====================================================
# AI
# =====================================================

DEFAULT_MODEL = "Gemini"

MAX_CONTEXT = 20

MAX_MEMORY = 1000


# =====================================================
# DATABASE
# =====================================================

DATABASE_NAME = "AetherMind.db"

DATABASE_PATH = DATA_DIR / DATABASE_NAME


# =====================================================
# LOGGING
# =====================================================

LOG_LEVEL = "INFO"

LOG_FILE = LOG_DIR / "system.log"


# =====================================================
# PLUGINS
# =====================================================

PLUGIN_AUTOLOAD = True

PLUGIN_SANDBOX = True


# =====================================================
# SYSTEM
# =====================================================

OS_NAME = "Windows"

SUPPORTED_OS = [

    "Windows",

    "Linux"

]


if __name__ == "__main__":

    print(PROJECT_NAME)

    print(VERSION)

    print(ROOT_DIR)

    print(DATA_DIR)
    
