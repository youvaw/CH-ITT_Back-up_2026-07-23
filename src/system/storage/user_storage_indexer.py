import os
import sys
import time
import traceback

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.storage.folder_discovery import FolderDiscovery
from src.system.storage.indexing_pipeline import IndexingPipeline


class UserStorageIndexer:
    """
    MYX Step 9.7

    Discovers important user storage locations and sends them
    through the existing IndexingPipeline.

    No individual file paths are hardcoded.
    """

    def __init__(self):
        self.folder_discovery = FolderDiscovery()
        self.pipeline = IndexingPipeline()

        print("[UserStorageIndexer] Initialized")

    def discover_locations(self):
        """
        Return discovered user storage locations.
        """
        locations = self.folder_discovery.get_locations()

        if not locations:
            return []

        return locations

    def _extract_path(self, location):
        """
        Supports dictionary/object/string location formats.
        """

        if isinstance(location, str):
            return location

        if isinstance(location, dict):
            for key in ("path", "full_path", "location"):
                value = location.get(key)

                if value:
                    return str(value)

        for attribute in ("path", "full_path", "location"):
            value = getattr(location, attribute, None)

            if value:
                return str(value)

        return None

    def index_location(self, location):
        """
        Index one discovered location.
        """

        path = self._extract_path(location)

        if not path:
            return {
                "success": False,
                "path": None,
                "discovered": 0,
                "indexed": 0,
                "error": "Unable to determine location path.",
            }

        if not os.path.isdir(path):
            return {
                "success": False,
                "path": path,
                "discovered": 0,
                "indexed": 0,
                "error": "Location does not exist.",
            }

        try:
            result = self.pipeline.index_folder(
                path,
                recursive=True,
            )

            if not isinstance(result, dict):
                result = {}

            discovered = result.get(
                "discovered",
                result.get("files_discovered", 0),
            )

            indexed = result.get(
                "indexed",
                result.get("files_indexed", 0),
            )

            success = bool(
                result.get(
                    "success",
                    indexed >= 0,
                )
            )

            return {
                "success": success,
                "path": path,
                "discovered": int(discovered or 0),
                "indexed": int(indexed or 0),
                "error": result.get("error"),
            }

        except Exception as exc:
            return {
                "success": False,
                "path": path,
                "discovered": 0,
                "indexed": 0,
                "error": str(exc),
            }

    def index_all(self):
        """
        Discover and index all important user locations.
        """

        start_time = time.time()

        locations = self.discover_locations()

        results = []

        total_discovered = 0
        total_indexed = 0

        successful_locations = 0
        failed_locations = 0

        print("\n==========================================")
        print("MYX USER STORAGE INDEXING")
        print("==========================================")

        print(f"Locations discovered : {len(locations)}")

        for location in locations:

            path = self._extract_path(location)

            print("\n------------------------------------------")
            print(f"Indexing: {path}")
            print("------------------------------------------")

            result = self.index_location(location)

            results.append(result)

            total_discovered += result["discovered"]
            total_indexed += result["indexed"]

            if result["success"]:
                successful_locations += 1

                print(
                    f"Discovered : {result['discovered']}"
                )

                print(
                    f"Indexed    : {result['indexed']}"
                )

                print("Status     : PASS")

            else:
                failed_locations += 1

                print(
                    f"Status     : FAIL"
                )

                if result["error"]:
                    print(
                        f"Reason     : {result['error']}"
                    )

        elapsed = time.time() - start_time

        final_result = {
            "locations_discovered": len(locations),
            "locations_indexed": successful_locations,
            "locations_failed": failed_locations,
            "files_discovered": total_discovered,
            "files_indexed": total_indexed,
            "elapsed_seconds": round(elapsed, 2),
            "success": successful_locations > 0,
            "results": results,
        }

        print("\n==========================================")
        print("USER STORAGE INDEXING SUMMARY")
        print("==========================================")

        print(
            f"Locations discovered : "
            f"{final_result['locations_discovered']}"
        )

        print(
            f"Locations indexed    : "
            f"{final_result['locations_indexed']}"
        )

        print(
            f"Locations failed     : "
            f"{final_result['locations_failed']}"
        )

        print(
            f"Files discovered     : "
            f"{final_result['files_discovered']}"
        )

        print(
            f"Files indexed        : "
            f"{final_result['files_indexed']}"
        )

        print(
            f"Time                 : "
            f"{final_result['elapsed_seconds']} sec"
        )

        return final_result


def main():

    print("==========================================")
    print("       MYX STEP 9.7 USER STORAGE TEST")
    print("==========================================")

    try:
        indexer = UserStorageIndexer()

        result = indexer.index_all()

        print("\n------------------------------------------")

        if result["success"]:
            print("STEP 9.7 TEST: PASS")
        else:
            print("STEP 9.7 TEST: FAIL")

        print("------------------------------------------")

    except Exception:
        print("\n==========================================")
        print("STEP 9.7 ERROR")
        print("==========================================")

        traceback.print_exc()


if __name__ == "__main__":
    main()
    

