import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.global_inventory import GlobalInventory


class GlobalSearch:
    """
    Unified search across MYX global inventory.
    """

    def __init__(self, inventory=None):
        self.inventory = inventory or GlobalInventory()

        print("[GlobalSearch] Initialized")

    def search(self, query, item_type=None, capability=None):
        query = self._normalize(query)

        if not query:
            return []

        results = []

        for record in self.inventory.all():

            if query not in record.normalized_name:
                continue

            if item_type:
                if record.item_type != (
                    self._normalize(item_type).lower()
                ):
                    continue

            if capability:
                capability = (
                    self._normalize(capability)
                    .lower()
                )

                if capability not in record.capabilities:
                    continue

            results.append(record)

        return results

    def search_type(self, query, item_type):
        return self.search(
            query,
            item_type=item_type
        )

    def search_capability(self, query, capability):
        return self.search(
            query,
            capability=capability
        )

    def count(self, query, item_type=None):
        return len(
            self.search(
                query,
                item_type=item_type
            )
        )

    @staticmethod
    def _normalize(value):
        if value is None:
            return ""

        return " ".join(
            str(value).strip().lower().split()
        )


if __name__ == "__main__":
    print("=" * 55)
    print("    MYX STEP 10.7 GLOBAL SEARCH TEST")
    print("=" * 55)

    from src.system.discovery_record import DiscoveryRecord

    inventory = GlobalInventory()

    records = [
        DiscoveryRecord(
            name="Google Chrome",
            item_type="application",
            capabilities=["open", "launch", "search"],
        ),
        DiscoveryRecord(
            name="Chrome Setup.exe",
            item_type="file",
            capabilities=["find", "open"],
        ),
        DiscoveryRecord(
            name="Python Tutorial.pdf",
            item_type="file",
            capabilities=["find", "open"],
        ),
        DiscoveryRecord(
            name="Visual Studio Code",
            item_type="application",
            capabilities=["open", "launch"],
        ),
    ]

    inventory.add_many(records)

    search = GlobalSearch(inventory)

    print("\n[TEST 1] Basic Global Search")

    result1 = search.search("chrome")

    test1 = len(result1) == 2

    print(
        "Results:",
        [item.name for item in result1]
    )

    print(
        "BASIC SEARCH TEST:",
        "PASS" if test1 else "FAIL"
    )

    print("\n[TEST 2] Type Search")

    result2 = search.search_type(
        "chrome",
        "application"
    )

    test2 = (
        len(result2) == 1
        and result2[0].name == "Google Chrome"
    )

    print(
        "Applications:",
        [item.name for item in result2]
    )

    print(
        "TYPE SEARCH TEST:",
        "PASS" if test2 else "FAIL"
    )

    print("\n[TEST 3] Capability Search")

    result3 = search.search_capability(
        "chrome",
        "open"
    )

    test3 = len(result3) == 2

    print(
        "Open-capable:",
        [item.name for item in result3]
    )

    print(
        "CAPABILITY SEARCH TEST:",
        "PASS" if test3 else "FAIL"
    )

    print("\n[TEST 4] PDF Search")

    result4 = search.search(
        "python tutorial",
        item_type="file"
    )

    test4 = (
        len(result4) == 1
        and result4[0].name == "Python Tutorial.pdf"
    )

    print(
        "PDF result:",
        [item.name for item in result4]
    )

    print(
        "PDF SEARCH TEST:",
        "PASS" if test4 else "FAIL"
    )

    print("\n[TEST 5] Empty Query Safety")

    result5 = search.search("")

    test5 = result5 == []

    print("Results:", result5)

    print(
        "EMPTY SEARCH TEST:",
        "PASS" if test5 else "FAIL"
    )

    tests = [test1, test2, test3, test4, test5]
    passed = sum(tests)

    print("\n" + "-" * 55)
    print(f"Tests passed : {passed}/5")

    if passed == 5:
        print("GLOBAL SEARCH TEST: PASS")
        print("STEP 10.7 TEST PASSED")
    else:
        print("GLOBAL SEARCH TEST: FAIL")
        print("STEP 10.7 TEST FAILED")

    print("-" * 55)
    
