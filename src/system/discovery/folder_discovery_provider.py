# ============================================================
# MYX - FOLDER DISCOVERY PROVIDER
# STEP 11.5
# ============================================================

import os
import sys
from typing import Any, Dict, List

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.storage.folder_discovery import FolderDiscovery
from src.system.discovery_record import DiscoveryRecord


class FolderDiscoveryProvider:

    def __init__(self, folder_discovery=None):

        self.folder_discovery = (
            folder_discovery or FolderDiscovery()
        )

        self.records: List[DiscoveryRecord] = []
        self.ready = True

        print("[FolderDiscoveryProvider] Initialized")

    # ========================================================
    # DISCOVER
    # ========================================================

    def discover(self) -> List[DiscoveryRecord]:

        try:
            locations = self.folder_discovery.get_locations()
        except Exception as error:
            print(
                f"[FolderDiscoveryProvider] "
                f"Discovery error: {error}"
            )
            locations = []

        records = []

        for item in locations:

            if not isinstance(item, dict):
                continue

            name = str(
                item.get("name", "")
            ).strip()

            path = str(
                item.get("path", "")
            ).strip()

            exists = item.get("exists", False)

            if not name or not path:
                continue

            if not exists:
                continue

            if not os.path.isdir(path):
                continue

            try:

                record = DiscoveryRecord(
                    name=name,
                    item_type="folder",
                    source="folder_discovery",
                    location=path,
                    target=path,
                    executable=None,
                    capabilities=[
                        "open",
                        "browse",
                        "search",
                    ],
                    metadata={
                        "folder_name": name,
                        "folder_type": "user_location",
                        "discovery_source": (
                            item.get(
                                "discovery_source",
                                "windows_user_profile",
                            )
                        ),
                    },
                    launchable=True,
                )

                records.append(record)

            except Exception as error:

                print(
                    "[FolderDiscoveryProvider] "
                    f"Record conversion error: {error}"
                )

        self.records = records

        print(
            f"[FolderDiscoveryProvider] "
            f"Folders discovered: {len(records)}"
        )

        return records

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, query: str) -> List[DiscoveryRecord]:

        query = str(query or "").strip().lower()

        if not query:
            return []

        if not self.records:
            self.discover()

        results = []

        for record in self.records:

            name = str(
                getattr(record, "name", "")
            ).lower()

            location = str(
                getattr(record, "location", "")
            ).lower()

            if query in name or query in location:
                results.append(record)

        return results

    # ========================================================
    # ALL
    # ========================================================

    def all(self) -> List[DiscoveryRecord]:
        return list(self.records)

    # ========================================================
    # STATUS
    # ========================================================

    def status(self) -> Dict[str, Any]:

        return {
            "provider": "folders",
            "ready": self.ready,
            "record_count": len(self.records),
        }

    # ========================================================
    # TEST
    # ========================================================

    def run_test(self) -> bool:

        print("=" * 65)
        print(
            "    MYX STEP 11.5 FOLDER DISCOVERY PROVIDER TEST"
        )
        print("=" * 65)

        passed = 0

        print("\n[TEST 1] Provider Initialization")

        if self.folder_discovery is not None:
            print("Folder source connected: PASS")
            passed += 1
        else:
            print("Folder source connected: FAIL")

        print("\n[TEST 2] Real Folder Discovery")

        records = self.discover()

        print(
            f"Folders discovered: {len(records)}"
        )

        if records:
            print("DISCOVERY TEST: PASS")
            passed += 1
        else:
            print("DISCOVERY TEST: FAIL")

        print("\n[TEST 3] Discovery Record Conversion")

        valid = [
            record
            for record in records
            if isinstance(record, DiscoveryRecord)
            and getattr(
                record,
                "item_type",
                None,
            ) == "folder"
        ]

        print(
            f"Valid folder records: {len(valid)}"
        )

        if len(valid) == len(records) and valid:
            print("RECORD CONVERSION TEST: PASS")
            passed += 1
        else:
            print("RECORD CONVERSION TEST: FAIL")

        print("\n[TEST 4] Desktop Detection")

        desktop = [
            record
            for record in records
            if str(
                getattr(record, "name", "")
            ).lower() == "desktop"
        ]

        if desktop:
            print(
                f"Desktop found: {desktop[0].location}"
            )
            print("DESKTOP TEST: PASS")
            passed += 1
        else:
            print("DESKTOP TEST: FAIL")

        print("\n[TEST 5] Provider Status")

        status = self.status()

        print(f"Status: {status}")

        if (
            status["ready"]
            and status["record_count"] > 0
        ):
            print("STATUS TEST: PASS")
            passed += 1
        else:
            print("STATUS TEST: FAIL")

        print("\n" + "-" * 65)
        print(f"Tests passed : {passed}/5")

        if passed == 5:
            print(
                "FOLDER DISCOVERY PROVIDER TEST: PASS"
            )
            print("STEP 11.5 TEST PASSED")
        else:
            print(
                "FOLDER DISCOVERY PROVIDER TEST: FAIL"
            )
            print("STEP 11.5 TEST FAILED")

        print("-" * 65)

        return passed == 5


if __name__ == "__main__":

    provider = FolderDiscoveryProvider()

    success = provider.run_test()

    raise SystemExit(
        0 if success else 1
    )