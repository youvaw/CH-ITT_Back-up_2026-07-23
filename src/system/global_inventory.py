import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.discovery_record import DiscoveryRecord


class GlobalInventory:
    """
    Unified inventory of all MYX discovered resources.

    Stores normalized discovery records and prevents
    duplicate entries.
    """

    def __init__(self):
        self.records = {}

        print("[GlobalInventory] Initialized")

    def _key(self, record):
        return (
            record.item_type,
            record.normalized_name,
            str(record.location or "").lower(),
            str(record.target or "").lower(),
        )

    def add(self, record):
        if not isinstance(record, DiscoveryRecord):
            return False

        key = self._key(record)

        if key in self.records:
            return False

        self.records[key] = record
        return True

    def add_many(self, records):
        added = 0

        for record in records:
            if self.add(record):
                added += 1

        return added

    def remove(self, record):
        if not isinstance(record, DiscoveryRecord):
            return False

        key = self._key(record)

        if key in self.records:
            del self.records[key]
            return True

        return False

    def clear(self):
        self.records.clear()

    def count(self):
        return len(self.records)

    def all(self):
        return list(self.records.values())

    def by_type(self, item_type):
        item_type = str(item_type).strip().lower()

        return [
            record
            for record in self.records.values()
            if record.item_type == item_type
        ]

    def find(self, name):
        query = str(name).strip().lower()

        if not query:
            return []

        return [
            record
            for record in self.records.values()
            if query in record.normalized_name
        ]

    def statistics(self):
        stats = {}

        for record in self.records.values():
            stats[record.item_type] = (
                stats.get(record.item_type, 0) + 1
            )

        return stats

    def status(self):
        return {
            "inventory": "global",
            "ready": True,
            "total": self.count(),
            "statistics": self.statistics(),
        }


if __name__ == "__main__":
    print("=" * 55)
    print("    MYX STEP 10.4 GLOBAL INVENTORY TEST")
    print("=" * 55)

    inventory = GlobalInventory()

    chrome = DiscoveryRecord(
        name="Google Chrome",
        item_type="application",
        source="test",
        capabilities=["open", "launch"],
        launchable=True,
    )

    vscode = DiscoveryRecord(
        name="Visual Studio Code",
        item_type="application",
        source="test",
        capabilities=["open", "launch"],
        launchable=True,
    )

    pdf = DiscoveryRecord(
        name="Python Tutorial.pdf",
        item_type="file",
        source="test",
        capabilities=["find", "open"],
    )

    print("\n[TEST 1] Inventory Initialization")

    test1 = inventory.count() == 0

    print("Initial count:", inventory.count())

    print(
        "INITIALIZATION TEST:",
        "PASS" if test1 else "FAIL"
    )

    print("\n[TEST 2] Add Records")

    added = inventory.add_many(
        [chrome, vscode, pdf]
    )

    test2 = (
        added == 3
        and inventory.count() == 3
    )

    print("Records added:", added)

    print(
        "ADD RECORD TEST:",
        "PASS" if test2 else "FAIL"
    )

    print("\n[TEST 3] Type Inventory")

    applications = inventory.by_type(
        "application"
    )

    test3 = len(applications) == 2

    print(
        "Applications:",
        [record.name for record in applications]
    )

    print(
        "TYPE INVENTORY TEST:",
        "PASS" if test3 else "FAIL"
    )

    print("\n[TEST 4] Name Search")

    results = inventory.find("chrome")

    test4 = (
        len(results) == 1
        and results[0].name == "Google Chrome"
    )

    print(
        "Search results:",
        [record.name for record in results]
    )

    print(
        "NAME SEARCH TEST:",
        "PASS" if test4 else "FAIL"
    )

    print("\n[TEST 5] Inventory Statistics")

    stats = inventory.statistics()

    test5 = (
        stats.get("application") == 2
        and stats.get("file") == 1
    )

    print("Statistics:", stats)

    print(
        "STATISTICS TEST:",
        "PASS" if test5 else "FAIL"
    )

    tests = [
        test1,
        test2,
        test3,
        test4,
        test5,
    ]

    passed = sum(tests)

    print("\n" + "-" * 55)
    print(f"Tests passed : {passed}/5")

    if passed == 5:
        print("GLOBAL INVENTORY TEST: PASS")
        print("STEP 10.4 TEST PASSED")
    else:
        print("GLOBAL INVENTORY TEST: FAIL")
        print("STEP 10.4 TEST FAILED")

    print("-" * 55)
    
