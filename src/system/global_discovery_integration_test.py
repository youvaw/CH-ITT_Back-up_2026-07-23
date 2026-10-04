import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.discovery_record import DiscoveryRecord
from src.system.discovery_source_registry import (
    DiscoverySourceRegistry,
)
from src.system.global_discovery_engine import (
    GlobalDiscoveryEngine,
)
from src.system.global_inventory import GlobalInventory
from src.system.capability_resolver import (
    CapabilityResolver,
)
from src.system.natural_command_capability import (
    NaturalCommandCapability,
)
from src.system.global_search import GlobalSearch
from src.system.global_action_resolver import (
    GlobalActionResolver,
)


def fake_application_provider():
    return [
        DiscoveryRecord(
            name="Google Chrome",
            item_type="application",
            source="test_application_provider",
            executable="chrome.exe",
            capabilities=[
                "open",
                "launch",
                "search",
            ],
            launchable=True,
        ),
        DiscoveryRecord(
            name="Visual Studio Code",
            item_type="application",
            source="test_application_provider",
            executable="code.exe",
            capabilities=[
                "open",
                "launch",
            ],
            launchable=True,
        ),
    ]


def fake_file_provider():
    return [
        DiscoveryRecord(
            name="Python Tutorial.pdf",
            item_type="file",
            source="test_file_provider",
            location=r"C:\Users\AVISHKAR\Documents",
            target=r"C:\Users\AVISHKAR\Documents\Python Tutorial.pdf",
            capabilities=[
                "find",
                "locate",
                "open",
            ],
        ),
        DiscoveryRecord(
            name="Python Project",
            item_type="folder",
            source="test_file_provider",
            location=r"C:\Users\AVISHKAR\Projects",
            target=r"C:\Users\AVISHKAR\Projects",
            capabilities=[
                "find",
                "locate",
                "open",
            ],
        ),
    ]


def main():
    print("=" * 60)
    print("      MYX STEP 10.9 GLOBAL DISCOVERY")
    print("              INTEGRATION TEST")
    print("=" * 60)

    registry = DiscoverySourceRegistry()

    engine = GlobalDiscoveryEngine(
        source_registry=registry
    )

    engine.register_provider(
        "applications",
        fake_application_provider,
    )

    engine.register_provider(
        "files",
        fake_file_provider,
    )

    print("\n[1] Discovery Engine")

    discovery_result = engine.run()

    test1 = (
        discovery_result["success"]
        and discovery_result["count"] == 4
    )

    print(
        "Discovered:",
        discovery_result["count"]
    )

    print(
        "DISCOVERY ENGINE:",
        "PASS" if test1 else "FAIL"
    )

    print("\n[2] Global Inventory")

    inventory = GlobalInventory()

    added = inventory.add_many(
        discovery_result["records"]
    )

    test2 = (
        added == 4
        and inventory.count() == 4
    )

    print("Inventory records:", inventory.count())

    print(
        "GLOBAL INVENTORY:",
        "PASS" if test2 else "FAIL"
    )

    print("\n[3] Capability Resolver")

    capability_resolver = CapabilityResolver(
        inventory
    )

    chrome = inventory.find("google chrome")[0]

    test3 = capability_resolver.can(
        chrome,
        "open"
    )

    print(
        "Chrome open capability:",
        test3
    )

    print(
        "CAPABILITY RESOLVER:",
        "PASS" if test3 else "FAIL"
    )

    print("\n[4] Natural Command")

    command_parser = NaturalCommandCapability()

    parsed = command_parser.resolve(
        "Open Google Chrome"
    )

    test4 = (
        parsed["success"]
        and parsed["capability"] == "open"
        and parsed["query"] == "google chrome"
    )

    print("Parsed:", parsed)

    print(
        "NATURAL COMMAND:",
        "PASS" if test4 else "FAIL"
    )

    print("\n[5] Global Search")

    search = GlobalSearch(inventory)

    search_result = search.search(
        "python"
    )

    test5 = len(search_result) == 2

    print(
        "Python results:",
        [item.name for item in search_result]
    )

    print(
        "GLOBAL SEARCH:",
        "PASS" if test5 else "FAIL"
    )

    print("\n[6] Global Action Resolver")

    action_resolver = GlobalActionResolver(
        search=search,
        capability_resolver=capability_resolver,
        command_parser=command_parser,
    )

    action_result = action_resolver.resolve(
        "Open Google Chrome"
    )

    test6 = (
        action_result["success"]
        and action_result["action"] == "open"
        and action_result["count"] == 1
    )

    print(
        "Action:",
        action_result["action"]
    )

    print(
        "Matches:",
        action_result["count"]
    )

    print(
        "GLOBAL ACTION:",
        "PASS" if test6 else "FAIL"
    )

    print("\n[7] Multiple Candidate Safety")

    multiple_result = action_resolver.resolve(
        "Find Python"
    )

    test7 = (
        multiple_result["success"]
        and multiple_result["count"] == 2
        and multiple_result["needs_selection"] is True
    )

    print(
        "Matches:",
        multiple_result["count"]
    )

    print(
        "Needs selection:",
        multiple_result["needs_selection"]
    )

    print(
        "SELECTION SAFETY:",
        "PASS" if test7 else "FAIL"
    )

    print("\n[8] Unknown Command Safety")

    unknown_result = action_resolver.resolve(
        "Tell me something"
    )

    test8 = (
        unknown_result["success"] is False
        and unknown_result["action"] is None
    )

    print("Unknown result:", unknown_result)

    print(
        "UNKNOWN COMMAND:",
        "PASS" if test8 else "FAIL"
    )

    print("\n[9] Final System Status")

    final_status = {
        "discovery_records": engine.count(),
        "inventory_records": inventory.count(),
        "supported_capabilities": (
            capability_resolver.supported_capabilities()
        ),
        "registry_sources": registry.count(),
    }

    test9 = (
        final_status["discovery_records"] == 4
        and final_status["inventory_records"] == 4
        and "open" in final_status[
            "supported_capabilities"
        ]
    )

    print("Final status:", final_status)

    print(
        "FINAL STATUS:",
        "PASS" if test9 else "FAIL"
    )

    tests = [
        test1,
        test2,
        test3,
        test4,
        test5,
        test6,
        test7,
        test8,
        test9,
    ]

    passed = sum(tests)

    print("\n" + "=" * 60)
    print(f"Integration tests passed : {passed}/9")

    if passed == 9:
        print("GLOBAL DISCOVERY INTEGRATION: PASS")
        print("STEP 10.9 TEST PASSED")
        print()
        print("STEP 10 COMPLETE")
    else:
        print("GLOBAL DISCOVERY INTEGRATION: FAIL")
        print("STEP 10.9 TEST FAILED")

    print("=" * 60)


if __name__ == "__main__":
    main()
    
