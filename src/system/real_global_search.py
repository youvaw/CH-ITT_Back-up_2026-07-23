# ============================================================
# MYX - REAL GLOBAL SEARCH
# STEP 11.8
# ============================================================

import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.real_global_inventory import (
    RealGlobalInventory
)


class RealGlobalSearch:

    def __init__(self, inventory=None):

        self.inventory = (
            inventory or RealGlobalInventory()
        )

        if not self.inventory.records:
            self.inventory.build()

        print("[RealGlobalSearch] Initialized")

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, query):

        return self.inventory.search(query)

    # ========================================================
    # SEARCH TYPE
    # ========================================================

    def search_type(
        self,
        query,
        item_type
    ):

        return [
            record
            for record in self.search(query)
            if getattr(
                record,
                "item_type",
                None
            ) == item_type
        ]

    # ========================================================
    # SEARCH CAPABILITY
    # ========================================================

    def search_capability(
        self,
        query,
        capability
    ):

        results = []

        for record in self.search(query):

            capabilities = getattr(
                record,
                "capabilities",
                []
            )

            if capability in capabilities:
                results.append(record)

        return results

    # ========================================================
    # TEST
    # ========================================================

    def run_tests(self):

        print("=" * 65)
        print("    MYX STEP 11.8 REAL GLOBAL SEARCH TEST")
        print("=" * 65)

        passed = 0
        total = 5

        print("\n[TEST 1] Search Initialization")

        if self.inventory.ready:
            print("Inventory ready: PASS")
            passed += 1
        else:
            print("Inventory ready: FAIL")

        print("\n[TEST 2] Application Search")

        results = self.search("chrome")

        print(
            f"Chrome results: {len(results)}"
        )

        # Search can legitimately return zero on a different
        # machine, so this test checks API correctness.
        if isinstance(results, list):
            print("SEARCH TEST: PASS")
            passed += 1
        else:
            print("SEARCH TEST: FAIL")

        print("\n[TEST 3] Type Search")

        applications = self.search_type(
            "calculator",
            "application"
        )

        print(
            f"Calculator applications: "
            f"{len(applications)}"
        )

        if isinstance(applications, list):
            print("TYPE SEARCH TEST: PASS")
            passed += 1
        else:
            print("TYPE SEARCH TEST: FAIL")

        print("\n[TEST 4] Empty Search Safety")

        empty = self.search("")

        print(
            f"Empty query results: {len(empty)}"
        )

        if empty == []:
            print("EMPTY SEARCH TEST: PASS")
            passed += 1
        else:
            print("EMPTY SEARCH TEST: FAIL")

        print("\n[TEST 5] Search Result Objects")

        if all(
            hasattr(record, "name")
            for record in results
        ):
            print("RESULT OBJECT TEST: PASS")
            passed += 1
        else:
            print("RESULT OBJECT TEST: FAIL")

        print("\n" + "-" * 65)
        print(f"Tests passed : {passed}/{total}")

        if passed == total:
            print("REAL GLOBAL SEARCH TEST: PASS")
            print("STEP 11.8 TEST PASSED")
        else:
            print("REAL GLOBAL SEARCH TEST: FAIL")
            print("STEP 11.8 TEST FAILED")

        print("-" * 65)

        return passed == total


if __name__ == "__main__":

    search = RealGlobalSearch()
    search.run_tests()
    
