"""
=========================================
CHITT - Audit Logger
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
from datetime import datetime
from pathlib import Path


class AuditLogger:

    def __init__(self, log_file="logs/security_audit.log"):

        self.log_file = Path(log_file)

        self.log_file.parent.mkdir(

            parents=True,

            exist_ok=True

        )

    # ---------------------------------
    # Internal Writer
    # ---------------------------------

    def _write(self, level, event, details=None):

        entry = {

            "timestamp": datetime.now().isoformat(),

            "level": level,

            "event": event,

            "details": details if details else {}

        }

        with open(

            self.log_file,

            "a",

            encoding="utf-8"

        ) as file:

            file.write(

                json.dumps(entry)

            )

            file.write("\n")

        return entry

    # ---------------------------------
    # General Log
    # ---------------------------------

    def log(self, event, details=None):

        return self._write(

            "INFO",

            event,

            details

        )

    # ---------------------------------
    # Warning
    # ---------------------------------

    def warning(self, event, details=None):

        return self._write(

            "WARNING",

            event,

            details

        )

    # ---------------------------------
    # Error
    # ---------------------------------

    def error(self, event, details=None):

        return self._write(

            "ERROR",

            event,

            details

        )

    # ---------------------------------
    # Security Event
    # ---------------------------------

    def security(self, event, details=None):

        return self._write(

            "SECURITY",

            event,

            details

        )

    # ---------------------------------
    # Read Logs
    # ---------------------------------

    def read(self):

        if not self.log_file.exists():

            return []

        with open(

            self.log_file,

            "r",

            encoding="utf-8"

        ) as file:

            return [

                json.loads(line)

                for line in file

                if line.strip()

            ]

    # ---------------------------------
    # Clear Logs
    # ---------------------------------

    def clear(self):

        self.log_file.write_text(

            "",

            encoding="utf-8"

        )

        return True

    # ---------------------------------
    # Total Entries
    # ---------------------------------

    def count(self):

        return len(self.read())

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "AuditLogger",

            "entries": self.count(),

            "status": "OK"

        }


if __name__ == "__main__":

    logger = AuditLogger()

    logger.log(

        "System Started"

    )

    logger.security(

        "Login Success",

        {

            "user": "admin"

        }

    )

    print(logger.health())
    
