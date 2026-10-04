"""
=========================================
CHITT - Update System
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from .update_manager import UpdateManager
from .version_manager import VersionManager
from .package_manager import PackageManager
from .downloader import Downloader
from .installer import Installer
from .rollback import RollbackManager
from .update_checker import UpdateChecker
from .update_settings import UpdateSettings
from .config import UpdateConfig
from .environment import UpdateEnvironment

__author__ = "AVISHKAR"
__version__ = "1.0.0"

__all__ = [

    "UpdateManager",

    "VersionManager",

    "PackageManager",

    "Downloader",

    "Installer",

    "RollbackManager",

    "UpdateChecker",

    "UpdateSettings",

    "UpdateConfig",

    "UpdateEnvironment"

]

