import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.global_search import GlobalSearch
from src.system.capability_resolver import CapabilityResolver
from src.system.natural_command_capability import (
    NaturalCommandCapability,
)


class GlobalActionResolver:
    """
    Converts a natural command into:

        capability
        query
        matching resources
        execution decision

    It does not execute actions itself.
    """

    def __init__(
        self,
        search=None,
        capability_resolver=None,
        command_parser=None,
    ):
        self.search = search
        self.capability_resolver = (
            capability_resolver
        )
        self.command_parser = (
            command_parser
            or NaturalCommandCapability()
        )

        print("[GlobalActionResolver] Initialized")

    def resolve(self, command):
        parsed = self.command_parser.resolve(command)

        if not parsed.get("success"):
            return {
                "success": False,
                "action": None,
                "capability": None,
                "query": parsed.get("query", ""),
                "results": [],
                "count": 0,
            }

        capability = parsed["capability"]
        query = parsed["query"]

        results = []

        if self.search is not None:
            results = self.search.search(
                query,
                capability=capability,
            )

        return {
            "success": True,
            "action": capability,
            "capability": capability,
            "query": query,
            "results": results,
            "count": len(results),
            "needs_selection": len(results) > 1,
        }

    def can_resolve(self, command):
        return self.command_parser.resolve(
            command
        ).get("success", False)

    def has_single_target(self, result):
        return (
            result.get("success", False)
            and result.get("count", 0) == 1
        )

    def needs_selection(self, result):
        return (
            result.get("count", 0) > 1
        )


if __name__ == "__main__":
    print("=" * 55)
    print("    MYX STEP 10.8 GLOBAL ACTION RESOLVER TEST")
    print("=" * 55)

    from src.system.discovery_record import DiscoveryRecord
    from src.system.global_inventory import GlobalInventory

    inventory = GlobalInventory()

    inventory.add(
        DiscoveryRecord(
            name="Google Chrome",
            item_type="application",
            capabilities=[
                "open",
                "launch",
            ],
        )
    )

    inventory.add(
        DiscoveryRecord(
            name="Chrome Help.pdf",
            item_type="file",
            capabilities=[
                "find",
                "open",
            ],
        )
    )

    inventory.add(
        DiscoveryRecord(
            name="Chrome Notes.txt",
            item_type="file",
            capabilities=[
                "find",
                "open",
            ],
        )
    )

    search = GlobalSearch(inventory)
    capability_resolver = CapabilityResolver(inventory)

    resolver = GlobalActionResolver(
        search=search,
        capability_resolver=capability_resolver,
    )

    print("\n[TEST 1] Resolver Initialization")

    test1 = (
        resolver.search is search
        and resolver.capability_resolver is capability_resolver
    )

    print("Resolver ready:", test1)

    print(
        "INITIALIZATION TEST:",
        "PASS" if test1 else "FAIL"
    )

    print("\n[TEST 2] Open Command Resolution")

    result2 = resolver.resolve(
        "Open Google Chrome"
    )

    test2 = (
        result2["success"]
        and result2["action"] == "open"
        and result2["query"] == "google chrome"
        and result2["count"] == 1
    )

    print("Result:", result2)

    print(
        "OPEN RESOLUTION TEST:",
        "PASS" if test2 else "FAIL"
    )

    print("\n[TEST 3] Find Command Resolution")

    result3 = resolver.resolve(
        "Find Chrome"
    )

    test3 = (
        result3["success"]
        and result3["action"] == "find"
        and result3["count"] == 2
    )

    print("Result count:", result3["count"])

    print(
        "FIND RESOLUTION TEST:",
        "PASS" if test3 else "FAIL"
    )

    print("\n[TEST 4] Multiple Target Detection")

    test4 = resolver.needs_selection(result3)

    print(
        "Needs selection:",
        test4
    )

    print(
        "SELECTION DETECTION TEST:",
        "PASS" if test4 else "FAIL"
    )

    print("\n[TEST 5] Unknown Command Safety")

    result5 = resolver.resolve(
        "Tell me something"
    )

    test5 = (
        result5["success"] is False
        and result5["action"] is None
    )

    print("Result:", result5)

    print(
        "UNKNOWN COMMAND TEST:",
        "PASS" if test5 else "FAIL"
    )

    tests = [test1, test2, test3, test4, test5]
    passed = sum(tests)

    print("\n" + "-" * 55)
    print(f"Tests passed : {passed}/5")

    if passed == 5:
        print("GLOBAL ACTION RESOLVER TEST: PASS")
        print("STEP 10.8 TEST PASSED")
    else:
        print("GLOBAL ACTION RESOLVER TEST: FAIL")
        print("STEP 10.8 TEST FAILED")

    print("-" * 55)
    
