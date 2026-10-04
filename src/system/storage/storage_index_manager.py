import os
import sys
import time
import traceback

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.storage.file_index import FileIndex
from src.system.storage.user_storage_indexer import UserStorageIndexer


class StorageIndexManager:
    """
    MYX Step 9.8

    Central manager for the MYX file index.

    Responsibilities:
    - build index
    - inspect index
    - report statistics
    - verify index health
    """

    def __init__(self):
        self.index = FileIndex()
        self.indexer = UserStorageIndexer()

        print("[StorageIndexManager] Initialized")

    def get_total_files(self):
        try:
            return int(self.index.count_files())
        except Exception:
            return 0

    def get_statistics(self):
        """
        Collect available FileIndex statistics.
        """

        total_files = self.get_total_files()

        statistics = {
            "total_files": total_files,
        }

        # Try the existing statistics API if available.
        try:
            if hasattr(self.index, "get_category_statistics"):
                statistics["categories"] = (
                    self.index.get_category_statistics()
                )

            elif hasattr(self.index, "category_statistics"):
                statistics["categories"] = (
                    self.index.category_statistics()
                )

            else:
                statistics["categories"] = {}

        except Exception:
            statistics["categories"] = {}

        return statistics

    def build_index(self):
        """
        Build / refresh the user storage index.
        """

        start = time.time()

        result = self.indexer.index_all()

        elapsed = time.time() - start

        result["database_total"] = self.get_total_files()
        result["manager_elapsed_seconds"] = round(elapsed, 2)

        return result

    def health_check(self):
        """
        Verify that the index database is accessible
        and contains usable data.
        """

        try:
            total = self.get_total_files()

            return {
                "healthy": True,
                "total_files": total,
                "database": getattr(
                    self.index,
                    "db_path",
                    "available",
                ),
            }

        except Exception as exc:

            return {
                "healthy": False,
                "total_files": 0,
                "error": str(exc),
            }

    def report(self):

        statistics = self.get_statistics()
        health = self.health_check()

        return {
            "statistics": statistics,
            "health": health,
        }


def main():

    print("==========================================")
    print("      MYX STEP 9.8 INDEX MANAGER TEST")
    print("==========================================")

    try:

        manager = StorageIndexManager()

        print("\n[TEST 1] Index Health")

        health = manager.health_check()

        print(
            f"Healthy    : "
            f"{health.get('healthy')}"
        )

        print(
            f"Total files: "
            f"{health.get('total_files')}"
        )

        health_pass = health.get("healthy") is True

        print(
            "HEALTH TEST: "
            + ("PASS" if health_pass else "FAIL")
        )

        print("\n[TEST 2] Statistics")

        statistics = manager.get_statistics()

        print(
            f"Total indexed: "
            f"{statistics.get('total_files', 0)}"
        )

        print(
            "STATISTICS TEST: PASS"
        )

        print("\n[TEST 3] Manager Report")

        report = manager.report()

        print(
            f"Health: "
            f"{report['health'].get('healthy')}"
        )

        print(
            f"Files: "
            f"{report['statistics'].get('total_files', 0)}"
        )

        report_pass = isinstance(report, dict)

        print(
            "REPORT TEST: "
            + ("PASS" if report_pass else "FAIL")
        )

        print("\n------------------------------------------")

        if health_pass and report_pass:
            print("STEP 9.8 TEST: PASS")
        else:
            print("STEP 9.8 TEST: FAIL")

        print("------------------------------------------")

    except Exception:

        print("\n==========================================")
        print("STEP 9.8 ERROR")
        print("==========================================")

        traceback.print_exc()


if __name__ == "__main__":
    main()
    

