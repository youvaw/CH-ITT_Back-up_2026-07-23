"""
AetherMind Database Backup System
"""

import shutil
from datetime import datetime

from .config import DATABASE_PATH, BACKUP_DIR


class DatabaseBackup:

    def __init__(self):
        self.database = DATABASE_PATH
        self.backup_dir = BACKUP_DIR

    def create_backup(self):
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_file = self.backup_dir / f"AetherMind_{timestamp}.db"

        shutil.copy2(self.database, backup_file)

        return backup_file

    def latest_backup(self):
        backups = sorted(
            self.backup_dir.glob("*.db"),
            reverse=True
        )

        if backups:
            return backups[0]

        return None

    def restore_backup(self, backup_file):
        shutil.copy2(backup_file, self.database)

        return True
"""
AetherMind Database Migration System
"""

from .manager import DatabaseManager


class DatabaseMigration:

    def __init__(self):
        self.db = DatabaseManager()

    def current_version(self):
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS db_version(
            id INTEGER PRIMARY KEY,
            version INTEGER
        )
        """)

        version = self.db.fetchone(
            "SELECT version FROM db_version WHERE id=1"
        )

        if version is None:
            self.db.execute("""
            INSERT INTO db_version(id, version)
            VALUES(1, 1)
            """)
            return 1

        return version["version"]

    def update_version(self, version):

        self.db.execute("""
        UPDATE db_version
        SET version=?
        WHERE id=1
        """, (version,))

    def migrate(self):

        version = self.current_version()

        print(f"Current Database Version : {version}")

        if version == 1:
            print("Database is Up-To-Date")

        self.db.commit()
        self.db.close()


if __name__ == "__main__":
    DatabaseMigration().migrate()
        
