# ============================================================
# MYX - REAL DISCOVERY FULL INTEGRATION TEST
# STEP 11.10
# ============================================================

import os
import sys
import time


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.real_global_inventory import (
    RealGlobalInventory
)

from src.system.discovery_health_report import (
    DiscoveryHealthReport
)

from src.system.real_global_search import (
    RealGlobalSearch
)

from src.system.real_global_action_resolver import (
    RealGlobalActionResolver
)


def main():

    print("=" * 75)
    print("        MYX STEP 11.10 REAL SYSTEM INTEGRATION TEST")
    print("=" * 75)

    start = time.perf_counter()

    passed = 0
    total = 9

    # ========================================================
    # 1. INVENTORY
    # ========================================================

    print("\n[TEST 1] Real Global Inventory")

    inventory = RealGlobalInventory()

    records = inventory.build()

    print(
        f"Global records discovered: {len(records)}"
    )

    if records:
        print("INVENTORY TEST: PASS")
        passed += 1
    else:
        print("INVENTORY TEST: FAIL")

    # ========================================================
    # 2. APPLICATIONS
    # ========================================================

    print("\n[TEST 2] Applications")

    applications = [
        record
        for record in records
        if getattr(
            record,
            "item_type",
            None
        ) == "application"
    ]

    print(
        f"Applications: {len(applications)}"
    )

    if applications:
        print("APPLICATION TEST: PASS")
        passed += 1
    else:
        print("APPLICATION TEST: FAIL")

    # ========================================================
    # 3. FILES
    # ========================================================

    print("\n[TEST 3] Files")

    files = [
        record
        for record in records
        if getattr(
            record,
            "item_type",
            None
        ) == "file"
    ]

    print(
        f"Files: {len(files)}"
    )

    if files:
        print("FILE TEST: PASS")
        passed += 1
    else:
        print("FILE TEST: FAIL")

    # ========================================================
    # 4. STORAGE
    # ========================================================

    print("\n[TEST 4] Storage")

    storage = [
        record
        for record in records
        if (
            getattr(
                record,
                "metadata",
                {}
            ).get("resource_type")
            == "storage"
        )
    ]

    print(
        f"Storage records: {len(storage)}"
    )

    if storage:
        print("STORAGE TEST: PASS")
        passed += 1
    else:
        print("STORAGE TEST: FAIL")

    # ========================================================
    # 5. HEALTH
    # ========================================================

    print("\n[TEST 5] Discovery Health")

    health = DiscoveryHealthReport(
        inventory=inventory
    )

    report = health.generate()

    print(
        f"Healthy: {report['healthy']}"
    )

    if report["inventory_ready"]:
        print("HEALTH TEST: PASS")
        passed += 1
    else:
        print("HEALTH TEST: FAIL")

    # ========================================================
    # 6. GLOBAL SEARCH
    # ========================================================

    print("\n[TEST 6] Global Search")

    search = RealGlobalSearch(
        inventory=inventory
    )

    search_results = search.search(
        "chrome"
    )

    print(
        f"Chrome search results: "
        f"{len(search_results)}"
    )

    if isinstance(search_results, list):
        print("GLOBAL SEARCH TEST: PASS")
        passed += 1
    else:
        print("GLOBAL SEARCH TEST: FAIL")

    # ========================================================
    # 7. FILE SEARCH
    # ========================================================

    print("\n[TEST 7] File Search")

    file_results = search.search_type(
        "python",
        "file"
    )

    print(
        f"Python file results: "
        f"{len(file_results)}"
    )

    if isinstance(file_results, list):
        print("FILE SEARCH TEST: PASS")
        passed += 1
    else:
        print("FILE SEARCH TEST: FAIL")

    # ========================================================
    # 8. ACTION RESOLUTION
    # ========================================================

    print("\n[TEST 8] Global Action Resolution")

    resolver = RealGlobalActionResolver(
        search=search
    )

    action = resolver.resolve(
        "find chrome"
    )

    print(
        f"Action: {action['action']}"
    )

    print(
        f"Query: {action['query']}"
    )

    print(
        f"Results: {action['count']}"
    )

    if (
        action["success"]
        and action["action"] == "find"
    ):
        print("ACTION RESOLUTION TEST: PASS")
        passed += 1
    else:
        print("ACTION RESOLUTION TEST: FAIL")

    # ========================================================
    # 9. RECORD INTEGRITY
    # ========================================================

    print("\n[TEST 9] Record Integrity")

    valid_records = 0

    for record in records:

        if (
            hasattr(record, "name")
            and hasattr(record, "item_type")
            and hasattr(record, "source")
        ):
            valid_records += 1

    print(
        f"Valid records: "
        f"{valid_records}/{len(records)}"
    )

    if (
        records
        and valid_records == len(records)
    ):
        print("RECORD INTEGRITY TEST: PASS")
        passed += 1
    else:
        print("RECORD INTEGRITY TEST: FAIL")

    # ========================================================
    # FINAL
    # ========================================================

    elapsed = time.perf_counter() - start

    print("\n" + "=" * 75)

    print(
        f"Tests passed : {passed}/{total}"
    )

    print(
        f"Execution time: {elapsed:.2f} sec"
    )

    print(
        f"Applications  : {len(applications)}"
    )

    print(
        f"Files         : {len(files)}"
    )

    print(
        f"Storage       : {len(storage)}"
    )

    print(
        f"Total records : {len(records)}"
    )

    print("=" * 75)

    if passed == total:

        print(
            "REAL DISCOVERY INTEGRATION TEST: PASS"
        )

        print(
            "STEP 11.10 TEST PASSED"
        )

    else:

        print(
            "REAL DISCOVERY INTEGRATION TEST: FAIL"
        )

        print(
            "STEP 11.10 TEST FAILED"
        )

    print("=" * 75)

    return passed == total


if __name__ == "__main__":
    main()
    
