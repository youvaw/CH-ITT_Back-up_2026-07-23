"""
=========================================
AetherMind - Database Core
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.1.0
=========================================
"""

import sqlite3

from .config import (
    DATABASE_PATH,
    SQLITE_TIMEOUT,
    CHECK_SAME_THREAD,
    ENABLE_FOREIGN_KEYS,
    ENABLE_WAL_MODE,
    SYNCHRONOUS,
    TEMP_STORE,
)


class Database:

    def __init__(self):
        # ---------------------------------
        # Database Path
        # ---------------------------------
        self.db_path = DATABASE_PATH

        # Make sure parent directory exists
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # ---------------------------------
        # SQLite Connection
        # ---------------------------------
        self.connection = sqlite3.connect(
            self.db_path,
            timeout=SQLITE_TIMEOUT,
            check_same_thread=CHECK_SAME_THREAD,
        )

        # Return rows like dictionaries
        self.connection.row_factory = sqlite3.Row

        # ---------------------------------
        # SQLite Configuration
        # ---------------------------------

        if ENABLE_FOREIGN_KEYS:
            self.connection.execute(
                "PRAGMA foreign_keys = ON"
            )

        if ENABLE_WAL_MODE:
            self.connection.execute(
                "PRAGMA journal_mode = WAL"
            )

        self.connection.execute(
            f"PRAGMA synchronous = {SYNCHRONOUS}"
        )

        self.connection.execute(
            f"PRAGMA temp_store = {TEMP_STORE}"
        )

        self.cursor = self.connection.cursor()

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, query, params=()):
        self.cursor.execute(query, params)

        self.connection.commit()

        return self.cursor

    # ---------------------------------
    # Fetch One
    # ---------------------------------

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)

        return self.cursor.fetchone()

    # ---------------------------------
    # Fetch All
    # ---------------------------------

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    # ---------------------------------
    # Commit
    # ---------------------------------

    def commit(self):
        self.connection.commit()

    # ---------------------------------
    # Rollback
    # ---------------------------------

    def rollback(self):
        self.connection.rollback()

    # ---------------------------------
    # Close
    # ---------------------------------

    def close(self):
        if self.connection:
            self.connection.close()
