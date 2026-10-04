# ============================================================
# MYX - REAL STORAGE DISCOVERY PROVIDER
# STEP 11.2
# ============================================================

import os
import sys
from typing import Any, Dict, List


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.storage.storage_discovery import StorageDiscovery
from src.system.discovery_record import DiscoveryRecord


class StorageDiscoveryProvider:

    def __init__(self, storage_discovery=None):
        self.storage_discovery = (
            storage_discovery or StorageDiscovery()
        )

        self.records: List[DiscoveryRecord] = []
        self.ready = True

        print("[StorageDiscoveryProvider] Initialized")

    # ========================================================
    # HELPERS
    # ========================================================

    @staticmethod
    def _value(obj, *names, default=None):

        if isinstance(obj, dict):
            for name in names:
                if name in obj:
                    return obj[name]

        for name in names:
            if hasattr(obj, name):
                return getattr(obj, name)

        return default

    # ========================================================
    # DISCOVER
    # ========================================================

    def discover(self) -> List[DiscoveryRecord]:

        try:
            if hasattr(self.storage_discovery, "discover"):
                raw = self.storage_discovery.discover()

            elif hasattr(self.storage_discovery, "get_drives"):
                raw = self.storage_discovery.get_drives()

            elif hasattr(self.storage_discovery, "list_drives"):
                raw = self.storage_discovery.list_drives()

            else:
                raw = []

        except Exception as error:
            print(
                f"[StorageDiscoveryProvider] "
                f"Discovery error: {error}"
            )
            raw = []

        if raw is None:
            raw = []

        if isinstance(raw, dict):
            raw = list(raw.values())

        if not isinstance(raw, (list, tuple)):
            raw = [raw]

        records = []

        for drive in raw:

            mount = self._value(
                drive,
                "mount",
                "path",
                "drive",
                "root",
                default=""
            )

            mount = str(mount).strip()

            if not mount:
                continue

            if not mount.endswith("\\"):
                mount += "\\"

            filesystem = self._value(
                drive,
                "filesystem",
                "file_system",
                "fs",
                default=""
            )

            total = self._value(
                drive,
                "total",
                "total_bytes",
                "total_size",
                default=None
            )

            free = self._value(
                drive,
                "free",
                "free_bytes",
                "free_space",
                default=None
            )

            used = self._value(
                drive,
                "used",
                "used_bytes",
                "used_space",
                default=None
            )

            drive_type = self._value(
                drive,
                "type",
                "drive_type",
                "kind",
                default="fixed"
            )

            metadata = {
                "resource_type": "storage",
                "drive": mount,
                "drive_type": drive_type,
                "filesystem": filesystem,
                "total": total,
                "used": used,
                "free": free,
            }

            try:

                record = DiscoveryRecord(
                    name=mount,
                    item_type="folder",
                    source="storage",
                    location=mount,
                    target=mount,
                    executable=None,
                    capabilities=[
                        "open",
                        "browse",
                        "search",
                    ],
                    metadata=metadata,
                    launchable=True,
                )

                records.append(record)

            except Exception as error:

                print(
                    "[StorageDiscoveryProvider] "
                    f"Record conversion error: {error}"
                )

        self.records = records

        return records

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, query: str):

        query = str(query or "").strip().lower()

        if not query:
            return []

        return [
            record
            for record in self.records
            if query in record.name.lower()
            or query in str(
                record.metadata.get("drive", "")
            ).lower()
        ]

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        return {
            "provider": "storage",
            "ready": self.ready,
            "record_count": len(self.records),
        }

    # ========================================================
    # TESTS
    # ========================================================

    def run_tests(self):

        print("=" * 65)
        print("    MYX STEP 11.2 STORAGE DISCOVERY PROVIDER TEST")
        print("=" * 65)

        passed = 0
        total = 5

        print("\n[TEST 1] Provider Initialization")

        if self.storage_discovery is not None:
            print("Storage source connected: PASS")
            passed += 1
        else:
            print("Storage source connected: FAIL")

        print("\n[TEST 2] Real Storage Discovery")

        records = self.discover()

        print(
            f"Storage records discovered: {len(records)}"
        )

        if len(records) > 0:
            print("DISCOVERY TEST: PASS")
            passed += 1
        else:
            print("DISCOVERY TEST: FAIL")

        print("\n[TEST 3] Discovery Record Conversion")

        valid = [
            record
            for record in records
            if isinstance(record, DiscoveryRecord)
        ]

        print(
            f"Valid DiscoveryRecords: {len(valid)}"
        )

        if len(valid) == len(records) and valid:
            print("RECORD CONVERSION TEST: PASS")
            passed += 1
        else:
            print("RECORD CONVERSION TEST: FAIL")

        print("\n[TEST 4] Drive Information")

        sample = [
            {
                "name": record.name,
                "filesystem": record.metadata.get(
                    "filesystem"
                ),
            }
            for record in records[:5]
        ]

        print(f"Sample drives: {sample}")

        if sample:
            print("DRIVE INFORMATION TEST: PASS")
            passed += 1
        else:
            print("DRIVE INFORMATION TEST: FAIL")

        print("\n[TEST 5] Provider Status")

        status = self.status()

        print(f"Status: {status}")

        if status["ready"] and status["record_count"] > 0:
            print("STATUS TEST: PASS")
            passed += 1
        else:
            print("STATUS TEST: FAIL")

        print("\n" + "-" * 65)
        print(f"Tests passed : {passed}/{total}")

        if passed == total:
            print("STORAGE DISCOVERY PROVIDER TEST: PASS")
            print("STEP 11.2 TEST PASSED")
        else:
            print("STORAGE DISCOVERY PROVIDER TEST: FAIL")
            print("STEP 11.2 TEST FAILED")

        print("-" * 65)

        return passed == total


if __name__ == "__main__":

    provider = StorageDiscoveryProvider()
    provider.run_tests()
    

