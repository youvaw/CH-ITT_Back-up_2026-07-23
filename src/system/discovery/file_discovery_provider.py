import os
import sys
import time
from typing import Any, Dict, List

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.storage.folder_discovery import FolderDiscovery
from src.system.storage.file_discovery import FileDiscovery
from src.system.discovery_record import DiscoveryRecord


class FileDiscoveryProvider:
    """
    MYX Real File Discovery Provider

    Responsibility:
        FolderDiscovery
              â†“
        FileDiscovery
              â†“
        DiscoveryRecord

    This provider is read-only.
    It discovers files and converts them into the global
    DiscoveryRecord format.

    It does NOT:
        - open files
        - modify files
        - delete files
        - launch applications
        - modify the global discovery engine
    """

    def __init__(
        self,
        folder_discovery=None,
        file_discovery=None,
    ):
        self.folder_discovery = (
            folder_discovery or FolderDiscovery()
        )

        self.file_discovery = (
            file_discovery or FileDiscovery()
        )

        self.records: List[DiscoveryRecord] = []
        self.last_errors: List[str] = []

        print("[FileDiscoveryProvider] Initialized")

    # ---------------------------------------------------------
    # BASIC HELPERS
    # ---------------------------------------------------------

    @staticmethod
    def _normalize(value: Any) -> str:
        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def _path_exists(path: str) -> bool:
        path = str(path).strip()

        if not path:
            return False

        try:
            return os.path.exists(path)
        except Exception:
            return False

    # ---------------------------------------------------------
    # LOCATION EXTRACTION
    # ---------------------------------------------------------

    def _extract_path(self, item: Any) -> str:
        """
        Convert different FolderDiscovery return formats
        into a usable filesystem path.
        """

        if item is None:
            return ""

        # Direct string path
        if isinstance(item, str):
            value = item.strip()

            if self._path_exists(value):
                return value

            return ""

        # Dictionary result
        if isinstance(item, dict):

            possible_keys = [
                "path",
                "full_path",
                "folder_path",
                "location",
                "target",
                "root",
            ]

            for key in possible_keys:
                value = item.get(key)

                if value:
                    value = self._normalize(value)

                    if self._path_exists(value):
                        return value

        # Object result
        possible_attributes = [
            "path",
            "full_path",
            "folder_path",
            "location",
            "target",
            "root",
        ]

        for attribute in possible_attributes:
            try:
                value = getattr(item, attribute, None)

                if value:
                    value = self._normalize(value)

                    if self._path_exists(value):
                        return value

            except Exception:
                continue

        return ""

    # ---------------------------------------------------------
    # FOLDER DISCOVERY
    # ---------------------------------------------------------

    def _discover_locations(self) -> List[str]:
        """
        Obtain usable filesystem locations from FolderDiscovery.

        The adapter intentionally supports several possible
        FolderDiscovery APIs so the provider is not tightly
        coupled to one implementation.
        """

        locations: List[str] = []

        candidate_methods = [
            "discover",
            "discover_locations",
            "get_locations",
            "discover_user_locations",
            "get_user_locations",
            "all",
        ]

        result = None

        for method_name in candidate_methods:

            method = getattr(
                self.folder_discovery,
                method_name,
                None,
            )

            if not callable(method):
                continue

            try:
                result = method()
                break
            except TypeError:
                continue
            except Exception as error:
                self.last_errors.append(
                    f"Folder discovery '{method_name}' failed: {error}"
                )

        if result is None:
            return []

        # Dictionary result
        if isinstance(result, dict):

            # Common structure:
            # {"desktop": "...", "documents": "..."}
            for value in result.values():

                path = self._extract_path(value)

                if path:
                    locations.append(path)

        # List / tuple / set result
        elif isinstance(result, (list, tuple, set)):

            for item in result:

                path = self._extract_path(item)

                if path:
                    locations.append(path)

        else:

            path = self._extract_path(result)

            if path:
                locations.append(path)

        # -----------------------------------------------------
        # Add important Windows locations as fallback/coverage.
        # These are only used if they exist.
        # -----------------------------------------------------

        fallback_locations = [
            os.path.expanduser("~"),
            os.path.join(
                os.path.expanduser("~"),
                "Desktop",
            ),
            os.path.join(
                os.path.expanduser("~"),
                "Documents",
            ),
            os.path.join(
                os.path.expanduser("~"),
                "Downloads",
            ),
            os.path.join(
                os.path.expanduser("~"),
                "Pictures",
            ),
            os.path.join(
                os.path.expanduser("~"),
                "Music",
            ),
            os.path.join(
                os.path.expanduser("~"),
                "Videos",
            ),
            os.path.join(
                os.path.expanduser("~"),
                "OneDrive",
            ),
        ]

        locations.extend(fallback_locations)

        # -----------------------------------------------------
        # Normalize + deduplicate
        # -----------------------------------------------------

        unique_locations = []
        seen = set()

        for path in locations:

            path = self._normalize(path)

            if not path:
                continue

            try:
                normalized = os.path.normcase(
                    os.path.abspath(path)
                )
            except Exception:
                continue

            if normalized in seen:
                continue

            if not self._path_exists(path):
                continue

            seen.add(normalized)
            unique_locations.append(path)

        return unique_locations

    # ---------------------------------------------------------
    # FILE DISCOVERY
    # ---------------------------------------------------------

    def _discover_files_from_location(
        self,
        location: str,
    ) -> List[Any]:
        """
        Discover files from one location.

        Uses the existing FileDiscovery implementation rather
        than duplicating filesystem scanning logic.
        """

        if not self._path_exists(location):
            return []

        method = getattr(
            self.file_discovery,
            "discover_folder",
            None,
        )

        if not callable(method):
            self.last_errors.append(
                "FileDiscovery.discover_folder() is unavailable."
            )
            return []

        attempts = [
            # Normal known API
            lambda: method(location, recursive=False),

            # Alternative positional form
            lambda: method(location),

            # Recursive form where supported
            lambda: method(location, recursive=True),
        ]

        for attempt in attempts:

            try:
                result = attempt()

                if result is None:
                    return []

                if isinstance(result, list):
                    return result

                if isinstance(result, tuple):
                    return list(result)

                if isinstance(result, set):
                    return list(result)

                # Some implementations may return a single item
                return [result]

            except TypeError:
                continue

            except Exception as error:
                self.last_errors.append(
                    f"File discovery failed for '{location}': {error}"
                )
                return []

        return []

    # ---------------------------------------------------------
    # FILE RECORD CONVERSION
    # ---------------------------------------------------------

    def _extract_file_value(
        self,
        item: Any,
        keys: List[str],
    ) -> Any:

        if isinstance(item, dict):

            for key in keys:

                if key in item and item[key] is not None:
                    return item[key]

        for key in keys:

            try:
                value = getattr(item, key, None)

                if value is not None:
                    return value

            except Exception:
                continue

        return None

    def _convert_to_record(
        self,
        item: Any,
    ) -> DiscoveryRecord | None:
        """
        Convert a FileDiscovery result into DiscoveryRecord.
        """

        if isinstance(item, DiscoveryRecord):

            if item.item_type != "file":
                return None

            return item

        path = self._extract_file_value(
            item,
            [
                "path",
                "full_path",
                "file_path",
                "location",
            ],
        )

        name = self._extract_file_value(
            item,
            [
                "name",
                "filename",
                "file_name",
            ],
        )

        category = self._extract_file_value(
            item,
            [
                "category",
                "file_category",
                "type",
            ],
        )

        extension = self._extract_file_value(
            item,
            [
                "extension",
                "ext",
            ],
        )

        size = self._extract_file_value(
            item,
            [
                "size",
                "file_size",
            ],
        )

        modified = self._extract_file_value(
            item,
            [
                "modified",
                "modified_time",
                "mtime",
            ],
        )

        path = self._normalize(path)
        name = self._normalize(name)

        if not path:
            return None

        if not self._path_exists(path):
            return None

        if not name:
            name = os.path.basename(path)

        metadata = {
            "category": self._normalize(category),
            "extension": self._normalize(extension),
            "size": size,
            "modified": modified,
        }

        # Remove empty metadata values
        metadata = {
            key: value
            for key, value in metadata.items()
            if value not in ("", None)
        }

        try:
            record = DiscoveryRecord(
                name=name,
                item_type="file",
                source="file_discovery",
                location=path,
                target=path,
                capabilities=[
                    "find",
                    "search",
                    "locate",
                    "show",
                    "open",
                ],
                metadata=metadata,
                launchable=False,
            )

            return record

        except Exception as error:

            self.last_errors.append(
                f"DiscoveryRecord conversion failed for "
                f"'{path}': {error}"
            )

            return None

    # ---------------------------------------------------------
    # REAL DISCOVERY
    # ---------------------------------------------------------

    def discover(self) -> List[DiscoveryRecord]:

        start_time = time.time()

        self.records = []
        self.last_errors = []

        locations = self._discover_locations()

        discovered_items = []

        for location in locations:

            try:
                items = self._discover_files_from_location(
                    location
                )

                discovered_items.extend(items)

            except Exception as error:

                self.last_errors.append(
                    f"Location '{location}' failed: {error}"
                )

        # -----------------------------------------------------
        # Convert to DiscoveryRecord
        # -----------------------------------------------------

        converted = []

        seen_paths = set()

        for item in discovered_items:

            record = self._convert_to_record(item)

            if record is None:
                continue

            path = self._normalize(
                getattr(record, "location", "")
            )

            try:
                normalized = os.path.normcase(
                    os.path.abspath(path)
                )
            except Exception:
                normalized = path.lower()

            if normalized in seen_paths:
                continue

            seen_paths.add(normalized)

            converted.append(record)

        self.records = converted

        elapsed = time.time() - start_time

        print(
            f"[FileDiscoveryProvider] Locations : "
            f"{len(locations)}"
        )

        print(
            f"[FileDiscoveryProvider] Files discovered : "
            f"{len(discovered_items)}"
        )

        print(
            f"[FileDiscoveryProvider] Records created : "
            f"{len(self.records)}"
        )

        print(
            f"[FileDiscoveryProvider] Time : "
            f"{elapsed:.2f} sec"
        )

        return self.records

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------

    def all(self) -> List[DiscoveryRecord]:
        return list(self.records)

    def count(self) -> int:
        return len(self.records)

    def search(self, query: str) -> List[DiscoveryRecord]:

        query = self._normalize(query).lower()

        if not query:
            return []

        results = []

        for record in self.records:

            name = self._normalize(
                getattr(record, "name", "")
            ).lower()

            location = self._normalize(
                getattr(record, "location", "")
            ).lower()

            if query in name or query in location:
                results.append(record)

        return results

    def status(self) -> Dict[str, Any]:

        return {
            "provider": "files",
            "ready": True,
            "record_count": len(self.records),
            "error_count": len(self.last_errors),
            "errors": list(self.last_errors[:10]),
        }

    # ---------------------------------------------------------
    # TEST
    # ---------------------------------------------------------

    def run_test(self) -> bool:

        print("=" * 65)
        print("    MYX STEP 11.3 FILE DISCOVERY PROVIDER TEST")
        print("=" * 65)

        passed = 0

        # -----------------------------------------------------
        # TEST 1
        # -----------------------------------------------------

        print("\n[TEST 1] Provider Initialization")

        if (
            self.folder_discovery is not None
            and self.file_discovery is not None
        ):
            print("File sources connected: PASS")
            passed += 1
        else:
            print("File sources connected: FAIL")

        # -----------------------------------------------------
        # TEST 2
        # -----------------------------------------------------

        print("\n[TEST 2] Real File Discovery")

        records = self.discover()

        print(f"Files discovered: {len(records)}")

        if len(records) > 0:
            print("DISCOVERY TEST: PASS")
            passed += 1
        else:
            print("DISCOVERY TEST: FAIL")

            if self.last_errors:
                print("Discovery errors:")
                for error in self.last_errors[:5]:
                    print(f"  - {error}")

        # -----------------------------------------------------
        # TEST 3
        # -----------------------------------------------------

        print("\n[TEST 3] Discovery Record Conversion")

        valid_records = [
            record
            for record in records
            if isinstance(record, DiscoveryRecord)
            and getattr(record, "item_type", None) == "file"
        ]

        print(
            f"Valid file records: "
            f"{len(valid_records)}"
        )

        if valid_records:
            print("RECORD CONVERSION TEST: PASS")
            passed += 1
        else:
            print("RECORD CONVERSION TEST: FAIL")

        # -----------------------------------------------------
        # TEST 4
        # -----------------------------------------------------

        print("\n[TEST 4] File Names")

        sample_names = [
            getattr(record, "name", "")
            for record in valid_records[:10]
        ]

        print(
            f"Sample files: {sample_names}"
        )

        if sample_names:
            print("FILE NAME TEST: PASS")
            passed += 1
        else:
            print("FILE NAME TEST: FAIL")

        # -----------------------------------------------------
        # TEST 5
        # -----------------------------------------------------

        print("\n[TEST 5] Provider Status")

        status = self.status()

        print(f"Status: {status}")

        if (
            status.get("ready") is True
            and status.get("record_count", 0) > 0
        ):
            print("STATUS TEST: PASS")
            passed += 1
        else:
            print("STATUS TEST: FAIL")

        # -----------------------------------------------------
        # FINAL
        # -----------------------------------------------------

        print("\n" + "-" * 65)
        print(f"Tests passed : {passed}/5")

        if passed == 5:
            print("FILE DISCOVERY PROVIDER TEST: PASS")
            print("STEP 11.3 TEST PASSED")
        else:
            print("FILE DISCOVERY PROVIDER TEST: FAIL")
            print("STEP 11.3 TEST FAILED")

        print("-" * 65)

        return passed == 5


if __name__ == "__main__":

    provider = FileDiscoveryProvider()

    success = provider.run_test()

    raise SystemExit(0 if success else 1)


