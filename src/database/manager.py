# -*- coding: utf-8 -*-

"""
MyX Database Manager

Architecture:

    Brain
      ↓
    MemoryManager
      ↓
    DatabaseManager
      ↓
    DatabaseQueries
      ↓
    AetherMind.db
"""

from .database import Database
from .models import create_tables
from .queries import DatabaseQueries


class DatabaseManager:

    def __init__(self):
        self.db = Database()

        create_tables(self.db)

        self.query = DatabaseQueries(self.db)

    def execute(self, query, params=()):
        return self.db.execute(query, params)

    def fetchone(self, query, params=()):
        return self.db.fetchone(query, params)

    def fetchall(self, query, params=()):
        return self.db.fetchall(query, params)

    def commit(self):
        return self.db.commit()

    def rollback(self):
        return self.db.rollback()

    def close(self):
        return self.db.close()
