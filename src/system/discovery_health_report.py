# ============================================================
# MYX - DISCOVERY HEALTH / REPORT
# STEP 11.7
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


class DiscoveryHealthReport:

    def __init__(self, inventory=None):

        self.inventory = (
            inventory or RealGlobalInventory()
        )

        print("[DiscoveryHealthReport] Initialized")

    # ========================================================
    # REPORT
    # ========================================================

    def generate(self):

        status = self.inventory.status()

        provider_status = (
            self.inventory.engine
            .provider_manager
            .status()
        )

        providers = provider_status.get(
            "providers",
            {}
        )

        healthy = True

        provider_report = {}

        for name, data in providers.items():

            ready = bool(
                data.get("ready", False)
            )

            count = int(
                data.get("record_count", 0)
            )

            provider_report[name] = {
                "ready": ready,
                "record_count": count,
                "healthy": ready and count >= 0,
            }

            if not ready:
                healthy = False

        return {
            "healthy": healthy,
            "inventory_ready": self.inventory.ready,
            "total_records": len(
                self.inventory.records
            ),
            "types": self.inventory.statistics(),
            "providers": provider_report,
        }

    # ========================================================
    # PRINT
    # ========================================================

    def print_report(self):

        report = self.generate()

        print("\nMYX DISCOVERY HEALTH REPORT")
        print("=" * 55)

        print(
            f"Healthy       : {report['healthy']}"
        )

        print(
            f"Inventory     : "
            f"{report['inventory_ready']}"
        )

        print(
            f"Total records : "
            f"{report['total_records']}"
        )

        print("\nTypes:")

        for name, count in report["types"].items():
            print(
                f"  {name}: {count}"
            )

        print("\nProviders:")

        for name, data in report["providers"].items():
            print(
                f"  {name}: "
                f"ready={data['ready']} "
                f"records={data['record_count']}"
            )

        return report

    # ========================================================
    # TEST
    # ========================================================

    def run_tests(self):

        print("=" * 65)
        print("    MYX STEP 11.7 DISCOVERY HEALTH REPORT TEST")
        print("=" * 65)

        passed = 0
        total = 5

        print("\n[TEST 1] Health Component")

        if self.inventory is not None:
            print("Inventory connected: PASS")
            passed += 1
        else:
            print("Inventory connected: FAIL")

        print("\n[TEST 2] Inventory Build")

        self.inventory.build()

        if self.inventory.records:
            print("Inventory available: PASS")
            passed += 1
        else:
            print("Inventory available: FAIL")

        print("\n[TEST 3] Report Generation")

        report = self.generate()

        print(
            f"Total records: "
            f"{report['total_records']}"
        )

        if isinstance(report, dict):
            print("REPORT TEST: PASS")
            passed += 1
        else:
            print("REPORT TEST: FAIL")

        print("\n[TEST 4] Provider Report")

        if report["providers"]:
            print("PROVIDER REPORT TEST: PASS")
            passed += 1
        else:
            print("PROVIDER REPORT TEST: FAIL")

        print("\n[TEST 5] Health State")

        if report["inventory_ready"]:
            print("HEALTH STATE TEST: PASS")
            passed += 1
        else:
            print("HEALTH STATE TEST: FAIL")

        print("\n" + "-" * 65)
        print(f"Tests passed : {passed}/{total}")

        if passed == total:
            print("DISCOVERY HEALTH REPORT TEST: PASS")
            print("STEP 11.7 TEST PASSED")
        else:
            print("DISCOVERY HEALTH REPORT TEST: FAIL")
            print("STEP 11.7 TEST FAILED")

        print("-" * 65)

        return passed == total


if __name__ == "__main__":

    report = DiscoveryHealthReport()
    report.run_tests()
    
