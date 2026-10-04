# ============================================================
# MYX - DISCOVERY PROVIDER MANAGER
# STEP 12
# ============================================================

import os
import sys
from typing import Any, Dict, List


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# PROVIDERS
# ============================================================

from src.system.application_discovery_provider import (
    ApplicationDiscoveryProvider
)

from src.system.discovery.storage_discovery_provider import (
    StorageDiscoveryProvider
)

from src.system.discovery.folder_discovery_provider import (
    FolderDiscoveryProvider
)

from src.system.discovery.file_discovery_provider import (
    FileDiscoveryProvider
)


class DiscoveryProviderManager:

    def __init__(
        self,
        application_provider=None,
        storage_provider=None,
        folder_provider=None,
        file_provider=None,
    ):

        self.providers = {

            "applications": (
                application_provider
                or ApplicationDiscoveryProvider()
            ),

            "storage": (
                storage_provider
                or StorageDiscoveryProvider()
            ),

            "folders": (
                folder_provider
                or FolderDiscoveryProvider()
            ),

            "files": (
                file_provider
                or FileDiscoveryProvider()
            ),
        }

        self.records = []
        self.ready = True

        print(
            "[DiscoveryProviderManager] Initialized"
        )

    # ========================================================
    # DISCOVER ONE
    # ========================================================

    def discover_provider(self, name):

        provider = self.providers.get(name)

        if provider is None:
            return []

        try:

            return provider.discover()

        except Exception as error:

            print(
                f"[DiscoveryProviderManager] "
                f"{name} discovery error: {error}"
            )

            return []

    # ========================================================
    # DISCOVER ALL
    # ========================================================

    def discover_all(self):

        records = []

        for name in self.providers:

            provider_records = (
                self.discover_provider(name)
            )

            records.extend(
                provider_records
            )

        self.records = records

        return records

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, query):

        results = []

        for provider in self.providers.values():

            try:

                results.extend(
                    provider.search(query)
                )

            except Exception:

                continue

        return results

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        provider_status = {}

        for name, provider in self.providers.items():

            try:

                provider_status[name] = (
                    provider.status()
                )

            except Exception as error:

                provider_status[name] = {
                    "provider": name,
                    "ready": False,
                    "record_count": 0,
                    "error": str(error),
                }

        return {
            "manager": (
                "discovery_provider_manager"
            ),
            "ready": self.ready,
            "providers": provider_status,
            "record_count": len(self.records),
        }

    # ========================================================
    # TEST
    # ========================================================

    def run_tests(self):

        print("=" * 65)

        print(
            "    MYX STEP 12 DISCOVERY PROVIDER MANAGER TEST"
        )

        print("=" * 65)

        passed = 0
        total = 5

        # ----------------------------------------------------
        # TEST 1
        # ----------------------------------------------------

        print(
            "\n[TEST 1] Manager Initialization"
        )

        if len(self.providers) == 4:

            print(
                "Providers registered: PASS"
            )

            passed += 1

        else:

            print(
                "Providers registered: FAIL"
            )

        # ----------------------------------------------------
        # TEST 2
        # ----------------------------------------------------

        print(
            "\n[TEST 2] Provider Names"
        )

        names = list(
            self.providers.keys()
        )

        print(
            f"Providers: {names}"
        )

        required = {
            "applications",
            "storage",
            "folders",
            "files",
        }

        if required.issubset(
            self.providers
        ):

            print(
                "PROVIDER NAME TEST: PASS"
            )

            passed += 1

        else:

            print(
                "PROVIDER NAME TEST: FAIL"
            )

        # ----------------------------------------------------
        # TEST 3
        # ----------------------------------------------------

        print(
            "\n[TEST 3] Real Discovery"
        )

        records = self.discover_all()

        print(
            f"Total records: {len(records)}"
        )

        if records:

            print(
                "DISCOVERY TEST: PASS"
            )

            passed += 1

        else:

            print(
                "DISCOVERY TEST: FAIL"
            )

        # ----------------------------------------------------
        # TEST 4
        # ----------------------------------------------------

        print(
            "\n[TEST 4] Provider Status"
        )

        status = self.status()

        print(
            "Provider status count: "
            f"{len(status['providers'])}"
        )

        if len(
            status["providers"]
        ) == 4:

            print(
                "STATUS TEST: PASS"
            )

            passed += 1

        else:

            print(
                "STATUS TEST: FAIL"
            )

        # ----------------------------------------------------
        # TEST 5
        # ----------------------------------------------------

        print(
            "\n[TEST 5] Record Aggregation"
        )

        if (
            status["record_count"]
            == len(records)
        ):

            print(
                "RECORD AGGREGATION TEST: PASS"
            )

            passed += 1

        else:

            print(
                "RECORD AGGREGATION TEST: FAIL"
            )

        # ----------------------------------------------------
        # FINAL
        # ----------------------------------------------------

        print(
            "\n" + "-" * 65
        )

        print(
            f"Tests passed : {passed}/{total}"
        )

        if passed == total:

            print(
                "DISCOVERY PROVIDER MANAGER TEST: PASS"
            )

            print(
                "STEP 12 TEST PASSED"
            )

        else:

            print(
                "DISCOVERY PROVIDER MANAGER TEST: FAIL"
            )

            print(
                "STEP 12 TEST FAILED"
            )

        print(
            "-" * 65
        )

        return passed == total


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    manager = DiscoveryProviderManager()

    success = manager.run_tests()

    raise SystemExit(
        0 if success else 1
    )
