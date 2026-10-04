# ============================================================
# MYX - REAL GLOBAL DISCOVERY ENGINE
# STEP 11.5
# ============================================================

import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.discovery_provider_manager import (
    DiscoveryProviderManager
)


class RealGlobalDiscoveryEngine:

    def __init__(self, provider_manager=None):

        self.provider_manager = (
            provider_manager
            or DiscoveryProviderManager()
        )

        self.records = []
        self.ready = True

        print("[RealGlobalDiscoveryEngine] Initialized")

    # ========================================================
    # DISCOVER
    # ========================================================

    def discover(self):

        self.records = (
            self.provider_manager.discover_all()
        )

        return self.records

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, query):

        return self.provider_manager.search(query)

    # ========================================================
    # GET BY TYPE
    # ========================================================

    def get_by_type(self, item_type):

        return [
            record
            for record in self.records
            if getattr(record, "item_type", None)
            == item_type
        ]

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        return {
            "engine": "real_global_discovery",
            "ready": self.ready,
            "record_count": len(self.records),
            "provider_status":
                self.provider_manager.status(),
        }

    # ========================================================
    # TEST
    # ========================================================

    def run_tests(self):

        print("=" * 65)
        print("    MYX STEP 11.5 REAL GLOBAL DISCOVERY TEST")
        print("=" * 65)

        passed = 0
        total = 5

        print("\n[TEST 1] Engine Initialization")

        if self.provider_manager and self.ready:
            print("Engine ready: PASS")
            passed += 1
        else:
            print("Engine ready: FAIL")

        print("\n[TEST 2] Global Discovery")

        records = self.discover()

        print(
            f"Global records: {len(records)}"
        )

        if records:
            print("GLOBAL DISCOVERY TEST: PASS")
            passed += 1
        else:
            print("GLOBAL DISCOVERY TEST: FAIL")

        print("\n[TEST 3] Applications")

        applications = self.get_by_type(
            "application"
        )

        print(
            f"Applications: {len(applications)}"
        )

        if applications:
            print("APPLICATION TEST: PASS")
            passed += 1
        else:
            print("APPLICATION TEST: FAIL")

        print("\n[TEST 4] Files")

        files = self.get_by_type("file")

        print(
            f"Files: {len(files)}"
        )

        if files:
            print("FILE TEST: PASS")
            passed += 1
        else:
            print("FILE TEST: FAIL")

        print("\n[TEST 5] Status")

        status = self.status()

        print(
            f"Status record count: "
            f"{status['record_count']}"
        )

        if status["record_count"] == len(records):
            print("STATUS TEST: PASS")
            passed += 1
        else:
            print("STATUS TEST: FAIL")

        print("\n" + "-" * 65)
        print(f"Tests passed : {passed}/{total}")

        if passed == total:
            print("REAL GLOBAL DISCOVERY TEST: PASS")
            print("STEP 11.5 TEST PASSED")
        else:
            print("REAL GLOBAL DISCOVERY TEST: FAIL")
            print("STEP 11.5 TEST FAILED")

        print("-" * 65)

        return passed == total


if __name__ == "__main__":

    engine = RealGlobalDiscoveryEngine()
    engine.run_tests()
    
