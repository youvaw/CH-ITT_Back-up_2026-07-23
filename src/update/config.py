"""
=========================================
CHITT - Update Configuration
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from pathlib import Path


class UpdateConfig:

    VERSION = "1.0.0"

    MODULE = "UpdateSystem"

    ENABLED = True

    # ---------------------------------
    # Update Channels
    # ---------------------------------

    DEFAULT_CHANNEL = "stable"

    AVAILABLE_CHANNELS = [

        "stable",

        "beta",

        "dev"

    ]

    # ---------------------------------
    # Update Settings
    # ---------------------------------

    AUTO_UPDATE = False

    CHECK_INTERVAL_HOURS = 24

    VERIFY_CHECKSUM = True

    BACKUP_BEFORE_UPDATE = True

    ROLLBACK_ON_FAILURE = True

    # ---------------------------------
    # Network
    # ---------------------------------

    CONNECTION_TIMEOUT = 30

    DOWNLOAD_RETRIES = 3

    # ---------------------------------
    # Paths
    # ---------------------------------

    ROOT = Path.cwd()

    UPDATE_SYSTEM = ROOT / "update_system"

    DOWNLOADS = ROOT / "downloads"

    BACKUPS = ROOT / "backups"

    LOGS = ROOT / "logs"

    TEMP = ROOT / "temp"

    # ---------------------------------
    # Initialize Directories
    # ---------------------------------

    @classmethod
    def initialize(cls):

        cls.UPDATE_SYSTEM.mkdir(

            parents=True,

            exist_ok=True

        )

        cls.DOWNLOADS.mkdir(

            parents=True,

            exist_ok=True

        )

        cls.BACKUPS.mkdir(

            parents=True,

            exist_ok=True

        )

        cls.LOGS.mkdir(

            parents=True,

            exist_ok=True

        )

        cls.TEMP.mkdir(

            parents=True,

            exist_ok=True

        )

    # ---------------------------------
    # Configuration Information
    # ---------------------------------

    @classmethod
    def info(cls):

        return {

            "module": cls.MODULE,

            "version": cls.VERSION,

            "enabled": cls.ENABLED,

            "channel": cls.DEFAULT_CHANNEL,

            "downloads": str(cls.DOWNLOADS),

            "backups": str(cls.BACKUPS),

            "logs": str(cls.LOGS)

        }


if __name__ == "__main__":

    UpdateConfig.initialize()

    print(UpdateConfig.info())
    
