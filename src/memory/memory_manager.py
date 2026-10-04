# -*- coding: utf-8 -*-

"""
MyX Memory Manager
------------------

High-level memory layer between MyX Brain and Database.

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

from src.database.manager import DatabaseManager


class MemoryManager:

    def __init__(self, database=None):
        """
        Initialize MyX Memory Manager.

        If an existing DatabaseManager is provided, reuse it.
        Otherwise create a new DatabaseManager.
        """

        self.database = database or DatabaseManager()
        self.query = self.database.query

    # ---------------------------------------------------------
    # REMEMBER
    # ---------------------------------------------------------

    def remember(self, key, value):
        """
        Save or update a memory.
        """

        if key is None:
            return False

        key = str(key).strip()

        if not key:
            return False

        if value is None:
            value = ""

        value = str(value)

        return self.query.save_memory(
            key=key,
            value=value
        )

    # ---------------------------------------------------------
    # RECALL
    # ---------------------------------------------------------

    def recall(self, key, default=None):
        """
        Recall one memory value.
        """

        if key is None:
            return default

        key = str(key).strip()

        if not key:
            return default

        value = self.query.get_memory_value(key)

        if value is None:
            return default

        return value

    # ---------------------------------------------------------
    # RECALL ALL
    # ---------------------------------------------------------

    def recall_all(self):
        """
        Return all stored memories.
        """

        memories = self.query.get_all_memories()

        if memories is None:
            return []

        return memories

    # ---------------------------------------------------------
    # EXISTS
    # ---------------------------------------------------------

    def exists(self, key):
        """
        Check whether a memory exists.
        """

        if key is None:
            return False

        key = str(key).strip()

        if not key:
            return False

        return self.query.memory_exists(key)

    # ---------------------------------------------------------
    # FORGET
    # ---------------------------------------------------------

    def forget(self, key):
        """
        Delete one memory.
        """

        if key is None:
            return False

        key = str(key).strip()

        if not key:
            return False

        return self.query.delete_memory(key)

    # ---------------------------------------------------------
    # HEALTH
    # ---------------------------------------------------------

    def health(self):
        """
        Return memory-system health information.
        """

        return {
            "memory_manager": True,
            "database_connected": self.database is not None,
            "query_layer_connected": self.query is not None,
        }

    # ---------------------------------------------------------
    # CLOSE
    # ---------------------------------------------------------

    def close(self):
        """
        Safely close the database connection.
        """

        if self.database is not None:
            return self.database.close()

        return None


# =============================================================
# MEMORY MANAGER TEST
# =============================================================

def run_memory_manager_test():

    print("=" * 60)
    print("          MYX MEMORY MANAGER TEST")
    print("=" * 60)

    memory = None

    try:
        # -----------------------------------------------------
        # 1. Initialize
        # -----------------------------------------------------

        memory = MemoryManager()

        health = memory.health()

        if (
            health["memory_manager"]
            and health["database_connected"]
            and health["query_layer_connected"]
        ):
            print("[1] Database Health: PASS")
        else:
            print("[1] Database Health: FAIL")
            return

        # -----------------------------------------------------
        # 2. Remember
        # -----------------------------------------------------

        test_key = "myx_memory_test"
        test_value = "MyX memory system is working."

        saved = memory.remember(
            test_key,
            test_value
        )

        print(
            "[2] Remember:",
            "PASS" if saved else "FAIL"
        )

        # -----------------------------------------------------
        # 3. Recall
        # -----------------------------------------------------

        recalled = memory.recall(test_key)

        print(
            "[3] Recall:",
            "PASS" if recalled == test_value else "FAIL"
        )

        print(f"    Value: {recalled}")

        # -----------------------------------------------------
        # 4. Exists
        # -----------------------------------------------------

        exists = memory.exists(test_key)

        print(
            "[4] Exists:",
            "PASS" if exists else "FAIL"
        )

        # -----------------------------------------------------
        # 5. Recall All
        # -----------------------------------------------------

        memories = memory.recall_all()

        print(
            "[5] Recall All:",
            "PASS" if isinstance(memories, (list, tuple)) else "FAIL"
        )

        print(
            f"    Total Memories: {len(memories)}"
        )

        # -----------------------------------------------------
        # 6. Forget
        # -----------------------------------------------------

        deleted = memory.forget(test_key)

        print(
            "[6] Forget:",
            "PASS" if deleted else "FAIL"
        )

        # -----------------------------------------------------
        # 7. Verify deletion
        # -----------------------------------------------------

        after_delete = memory.recall(
            test_key,
            default=None
        )

        print(
            "[7] Verify Delete:",
            "PASS" if after_delete is None else "FAIL"
        )

        print("=" * 60)
        print("          MYX MEMORY MANAGER READY")
        print("=" * 60)

    except Exception as error:

        print("=" * 60)
        print("MYX MEMORY MANAGER ERROR")
        print("=" * 60)

        print(f"Error: {error}")

        raise

    finally:

        if memory is not None:

            try:
                memory.close()
            except Exception:
                pass


# =============================================================
# MODULE ENTRY POINT
# =============================================================

if __name__ == "__main__":
    run_memory_manager_test()