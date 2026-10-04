# ============================================================
# MYX - REAL GLOBAL INVENTORY
# STEP 11.6
# ============================================================

import os
import sys
from collections import Counter


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.real_global_discovery_engine import (
    RealGlobalDiscoveryEngine
)


class RealGlobalInventory:

    def __init__(self, engine=None):

        self.engine = (
            engine or RealGlobalDiscoveryEngine()
        )

        self.records = []
        self.by_type = {}
        self.by_name = {}

        self.ready = False

        print("[RealGlobalInventory] Initialized")

    # ========================================================
    # BUILD
    # ========================================================

    def build(self):

        self.records = self.engine.discover()

        self.by_type = {}
        self.by_name = {}

        for record in self.records:

            item_type = getattr(
                record,
                "item_type",
                "unknown"
            )

            self.by_type.setdefault(
                item_type,
                []
            ).append(record)

            name = str(
                getattr(record, "normalized_name", "")
                or getattr(record, "name", "")
            ).lower()

            if name:
                self.by_name.setdefault(
                    name,
                    []
                ).append(record)

        self.ready = True

        return self.records

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, query):

        query = str(query or "").strip().lower()

        if not query:
            return []

        results = []

        for record in self.records:

            name = str(
                getattr(record, "name", "")
            ).lower()

            location = str(
                getattr(record, "location", "")
            ).lower()

            target = str(
                getattr(record, "target", "")
            ).lower()

            if (
                query in name
                or query in location
                or query in target
            ):
                results.append(record)

        return results

    # ========================================================
    # STATISTICS
    # ========================================================

    def statistics(self):

        counter = Counter()

        for record in self.records:

            counter[
                getattr(
                    record,
                    "item_type",
                    "unknown"
                )
            ] += 1

        return dict(counter)

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        return {
            "inventory": "real_global_inventory",
            "ready": self.ready,
            "record_count": len(self.records),
            "types": self.statistics(),
        }

    # ========================================================
    # TEST
    # ========================================================

    def run_tests(self):

        print("=" * 65)
        print("    MYX STEP 11.6 REAL GLOBAL INVENTORY TEST")
        print("=" * 65)

        passed = 0
        total = 5

        print("\n[TEST 1] Inventory Initialization")

        if self.engine is not None:
            print("Engine connected: PASS")
            passed += 1
        else:
            print("Engine connected: FAIL")

        print("\n[TEST 2] Inventory Build")

        records = self.build()

        print(
            f"Inventory records: {len(records)}"
        )

        if records:
            print("BUILD TEST: PASS")
            passed += 1
        else:
            print("BUILD TEST: FAIL")

        print("\n[TEST 3] Type Statistics")

        stats = self.statistics()

        print(f"Statistics: {stats}")

        if stats:
            print("STATISTICS TEST: PASS")
            passed += 1
        else:
            print("STATISTICS TEST: FAIL")

        print("\n[TEST 4] Name Index")

        print(
            f"Indexed names: {len(self.by_name)}"
        )

        if self.by_name:
            print("NAME INDEX TEST: PASS")
            passed += 1
        else:
            print("NAME INDEX TEST: FAIL")

        print("\n[TEST 5] Inventory Status")

        status = self.status()

        print(f"Status: {status}")

        if status["ready"]:
            print("STATUS TEST: PASS")
            passed += 1
        else:
            print("STATUS TEST: FAIL")

        print("\n" + "-" * 65)
        print(f"Tests passed : {passed}/{total}")

        if passed == total:
            print("REAL GLOBAL INVENTORY TEST: PASS")
            print("STEP 11.6 TEST PASSED")
        else:
            print("REAL GLOBAL INVENTORY TEST: FAIL")
            print("STEP 11.6 TEST FAILED")

        print("-" * 65)

        return passed == total


if __name__ == "__main__":

    inventory = RealGlobalInventory()
    inventory.run_tests()
    
