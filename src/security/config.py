"""
=========================================
CHITT - Security Configuration
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from pathlib import Path


class SecurityConfig:

    VERSION = "1.0.0"

    MODULE = "Security"

    ENABLED = True

    # ---------------------------------
    # Security Level
    # ---------------------------------

    LEVEL = "HIGH"

    # ---------------------------------
    # Authentication
    # ---------------------------------

    SESSION_TIMEOUT = 3600

    MAX_LOGIN_ATTEMPTS = 5

    LOCKOUT_TIME = 300

    # ---------------------------------
    # Password Policy
    # ---------------------------------

    MIN_PASSWORD_LENGTH = 8

    REQUIRE_UPPERCASE = True

    REQUIRE_LOWERCASE = True

    REQUIRE_DIGITS = True

    REQUIRE_SYMBOLS = True

    # ---------------------------------
    # Encryption
    # ---------------------------------

    ENCRYPTION_ALGORITHM = "Fernet"

    KEY_SIZE = 32

    # ---------------------------------
    # Audit
    # ---------------------------------

    AUDIT_ENABLED = True

    LOG_FAILED_LOGIN = True

    LOG_PERMISSION_CHANGES = True

    # ---------------------------------
    # Paths
    # ---------------------------------

    ROOT = Path.cwd()

    SECURITY = ROOT / "security"

    LOGS = ROOT / "logs"

    KEYS = SECURITY / "keys"

    STORAGE = SECURITY / "storage"

    CERTIFICATES = SECURITY / "certificates"

    # ---------------------------------
    # Initialize Directories
    # ---------------------------------

    @classmethod
    def initialize(cls):

        cls.SECURITY.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.LOGS.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.KEYS.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.STORAGE.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.CERTIFICATES.mkdir(
            parents=True,
            exist_ok=True
        )

    # ---------------------------------
    # Information
    # ---------------------------------

    @classmethod
    def info(cls):

        return {

            "module": cls.MODULE,

            "version": cls.VERSION,

            "enabled": cls.ENABLED,

            "security_level": cls.LEVEL,

            "security_path": str(cls.SECURITY),

            "logs": str(cls.LOGS),

            "keys": str(cls.KEYS),

            "storage": str(cls.STORAGE)

        }


if __name__ == "__main__":

    SecurityConfig.initialize()

    print(SecurityConfig.info())
    
