"""
=========================================
AetherMind - Database Queries
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 2.1.0
=========================================
"""

import sqlite3


class DatabaseQueries:

    def __init__(self, db):
        self.db = db

    # ==================================================
    # USERS
    # ==================================================

    def create_user(
        self,
        user_id,
        name,
        password_hash,
        nickname="",
        email="",
        phone=""
    ):
        """
        Create a new MyX user.

        Password must already be hashed before calling
        this method.
        """

        if not user_id:
            raise ValueError("user_id cannot be empty.")

        if not name:
            raise ValueError("name cannot be empty.")

        if not password_hash:
            raise ValueError("password_hash cannot be empty.")

        try:
            self.db.execute(
                """
                INSERT INTO users
                (
                    user_id,
                    name,
                    nickname,
                    email,
                    phone,
                    password_hash
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    name,
                    nickname,
                    email,
                    phone,
                    password_hash
                ),
            )

            self.db.commit()
            return True

        except sqlite3.IntegrityError:
            return False

    # ---------------------------------
    # Get User
    # ---------------------------------

    def get_user(self, user_id):

        return self.db.fetchone(
            """
            SELECT *
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

    # ---------------------------------
    # Get User Password Hash
    # ---------------------------------

    def get_password_hash(self, user_id):

        user = self.get_user(user_id)

        if user is None:
            return None

        return user["password_hash"]

    # ---------------------------------
    # Check User Exists
    # ---------------------------------

    def user_exists(self, user_id):

        user = self.db.fetchone(
            """
            SELECT id
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        return user is not None

    # ==================================================
    # MEMORY
    # ==================================================

    def save_memory(self, key, value):
        """
        Save or update one long-term memory.

        Current AetherMind memory schema:

            id
            key
            value
            created_at

        The memory key uniquely identifies the
        remembered information at application level.
        """

        if not key:
            raise ValueError(
                "Memory key cannot be empty."
            )

        if value is None:
            raise ValueError(
                "Memory value cannot be None."
            )

        self.db.execute(
            """
            DELETE FROM memory
            WHERE key = ?
            """,
            (key,),
        )

        self.db.execute(
            """
            INSERT INTO memory
            (
                key,
                value
            )
            VALUES (?, ?)
            """,
            (
                str(key),
                str(value)
            ),
        )

        self.db.commit()

        return True

    # ---------------------------------
    # Get Memory
    # ---------------------------------

    def get_memory(self, key):
        """
        Get one memory by key.

        Returns:
            sqlite3.Row | None
        """

        if not key:
            return None

        return self.db.fetchone(
            """
            SELECT
                id,
                key,
                value,
                created_at
            FROM memory
            WHERE key = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (str(key),),
        )

    # ---------------------------------
    # Get Memory Value
    # ---------------------------------

    def get_memory_value(self, key):
        """
        Get only the stored value for a memory key.

        Returns:
            str | None
        """

        memory = self.get_memory(key)

        if memory is None:
            return None

        return memory["value"]

    # ---------------------------------
    # Get All Memories
    # ---------------------------------

    def get_all_memories(self):
        """
        Return all stored long-term memories.
        """

        return self.db.fetchall(
            """
            SELECT
                id,
                key,
                value,
                created_at
            FROM memory
            ORDER BY id ASC
            """
        )

    # ---------------------------------
    # Memory Exists
    # ---------------------------------

    def memory_exists(self, key):
        """
        Check whether a memory key exists.
        """

        if not key:
            return False

        row = self.db.fetchone(
            """
            SELECT id
            FROM memory
            WHERE key = ?
            LIMIT 1
            """,
            (str(key),),
        )

        return row is not None

    # ---------------------------------
    # Delete Memory
    # ---------------------------------

    def delete_memory(self, key):
        """
        Delete one memory by key.
        """

        if not key:
            return False

        cursor = self.db.execute(
            """
            DELETE FROM memory
            WHERE key = ?
            """,
            (str(key),),
        )

        self.db.commit()

        return cursor.rowcount > 0

    # ---------------------------------
    # Clear All Memories
    # ---------------------------------

    def clear_memories(self):
        """
        Delete all long-term memories.

        This is intentionally explicit because
        clearing memory is a destructive operation.
        """

        cursor = self.db.execute(
            """
            DELETE FROM memory
            """
        )

        self.db.commit()

        return cursor.rowcount

    # ==================================================
    # CONVERSATION HISTORY
    # ==================================================

    def save_message(
        self,
        user_id,
        role,
        message
    ):
        """
        Save one conversation message.
        """

        if not user_id:
            raise ValueError(
                "user_id cannot be empty."
            )

        if not role:
            raise ValueError(
                "role cannot be empty."
            )

        if message is None:
            raise ValueError(
                "message cannot be None."
            )

        self.db.execute(
            """
            INSERT INTO conversation_history
            (
                user_id,
                role,
                message
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                role,
                str(message)
            ),
        )

        self.db.commit()

        return True

    # ---------------------------------
    # Get Conversation History
    # ---------------------------------

    def get_history(self, user_id):

        if not user_id:
            return []

        return self.db.fetchall(
            """
            SELECT
                id,
                user_id,
                role,
                message,
                timestamp
            FROM conversation_history
            WHERE user_id = ?
            ORDER BY id ASC
            """,
            (user_id,),
        )

    # ---------------------------------
    # Get Recent Conversation History
    # ---------------------------------

    def get_recent_history(
        self,
        user_id,
        limit=20
    ):
        """
        Return the most recent conversation messages.

        Results are returned in chronological order.
        """

        if not user_id:
            return []

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = 20

        limit = max(1, min(limit, 500))

        rows = self.db.fetchall(
            """
            SELECT
                id,
                user_id,
                role,
                message,
                timestamp
            FROM conversation_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                user_id,
                limit
            ),
        )

        return list(reversed(rows))

    # ---------------------------------
    # Clear Conversation History
    # ---------------------------------

    def clear_history(self, user_id):

        if not user_id:
            return False

        cursor = self.db.execute(
            """
            DELETE FROM conversation_history
            WHERE user_id = ?
            """,
            (user_id,),
        )

        self.db.commit()

        return cursor.rowcount > 0

    # ==================================================
    # SETTINGS
    # ==================================================

    def save_setting(self, key, value):

        if not key:
            raise ValueError(
                "Setting key cannot be empty."
            )

        if value is None:
            raise ValueError(
                "Setting value cannot be None."
            )

        self.db.execute(
            """
            INSERT OR REPLACE INTO settings
            (
                setting_key,
                setting_value
            )
            VALUES (?, ?)
            """,
            (
                key,
                str(value)
            ),
        )

        self.db.commit()

        return True

    # ---------------------------------
    # Get Setting
    # ---------------------------------

    def get_setting(self, key):

        if not key:
            return None

        return self.db.fetchone(
            """
            SELECT setting_value
            FROM settings
            WHERE setting_key = ?
            """,
            (key,),
        )

    # ---------------------------------
    # Get Setting Value
    # ---------------------------------

    def get_setting_value(self, key):

        setting = self.get_setting(key)

        if setting is None:
            return None

        return setting["setting_value"]

    # ==================================================
    # SKILLS
    # ==================================================

    def add_skill(self, skill_name):

        if not skill_name:
            raise ValueError(
                "skill_name cannot be empty."
            )

        self.db.execute(
            """
            INSERT OR IGNORE INTO skills
            (
                skill_name
            )
            VALUES (?)
            """,
            (skill_name,),
        )

        self.db.commit()

        return True

    # ---------------------------------
    # Get Skills
    # ---------------------------------

    def get_skills(self):

        return self.db.fetchall(
            """
            SELECT *
            FROM skills
            ORDER BY skill_name ASC
            """
        )

    # ==================================================
    # LEGACY COMPATIBILITY
    # ==================================================

    def save_conversation(
        self,
        role,
        message
    ):
        """
        Legacy conversation storage.

        New code should use save_message()
        with user_id.
        """

        self.db.execute(
            """
            INSERT INTO conversations
            (
                role,
                message
            )
            VALUES (?, ?)
            """,
            (
                role,
                str(message)
            ),
        )

        self.db.commit()

        return True

    # ---------------------------------
    # Save Command
    # ---------------------------------

    def save_command(
        self,
        command,
        status
    ):

        self.db.execute(
            """
            INSERT INTO commands
            (
                command,
                status
            )
            VALUES (?, ?)
            """,
            (
                str(command),
                str(status)
            ),
        )

        self.db.commit()

        return True

    # ---------------------------------
    # Save Error
    # ---------------------------------

    def save_error(
        self,
        error,
        traceback
    ):

        self.db.execute(
            """
            INSERT INTO errors
            (
                error,
                traceback
            )
            VALUES (?, ?)
            """,
            (
                str(error),
                str(traceback)
            ),
        )

        self.db.commit()

        return True
    