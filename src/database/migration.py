"""
=========================================
AetherMind - Database Migration
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 2.0.0
=========================================
"""

from .manager import DatabaseManager


CURRENT_VERSION = 2


class DatabaseMigration:

    def __init__(self):
        self.db = DatabaseManager()

    # ---------------------------------
    # Get Current Database Version
    # ---------------------------------

    def current_version(self):
        row = self.db.fetchone(
            "SELECT version FROM db_version WHERE id = 1"
        )

        if row is None:
            self.db.execute(
                """
                INSERT INTO db_version (id, version)
                VALUES (1, ?)
                """,
                (CURRENT_VERSION,)
            )

            self.db.commit()
            return CURRENT_VERSION

        return row["version"]

    # ---------------------------------
    # Update Database Version
    # ---------------------------------

    def update_version(self, version):
        self.db.execute(
            """
            UPDATE db_version
            SET version = ?
            WHERE id = 1
            """,
            (version,)
        )

        self.db.commit()

    # ---------------------------------
    # Migration
    # ---------------------------------

    def migrate(self):

        version = self.current_version()

        print(f"Current Database Version : {version}")
        print(f"Required Database Version : {CURRENT_VERSION}")

        if version < CURRENT_VERSION:

            print("Running database migration...")

            # Future migrations will be added here.
            #
            # Example:
            #
            # if version < 3:
            #     self.migrate_to_v3()

            self.update_version(CURRENT_VERSION)

            print("Database migration completed.")

        elif version == CURRENT_VERSION:

            print("Database is Up-To-Date.")

        else:

            print(
                "WARNING: Database version is newer "
                "than this application."
            )

        self.db.close()


# ---------------------------------
# Run Migration Directly
# ---------------------------------

if __name__ == "__main__":
    DatabaseMigration().migrate()
    
