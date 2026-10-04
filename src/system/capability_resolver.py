import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.global_inventory import GlobalInventory


class CapabilityResolver:
    """
    Resolves what MYX can do with a discovered resource.
    """

    def __init__(self, inventory=None):
        self.inventory = inventory or GlobalInventory()

        print("[CapabilityResolver] Initialized")

    def capabilities_for(self, record):
        if record is None:
            return []

        return list(
            getattr(record, "capabilities", [])
        )

    def can(self, record, capability):
        capability = self._normalize(capability).lower()

        return capability in self.capabilities_for(record)

    def resolve(self, record, requested_capability=None):
        available = self.capabilities_for(record)

        if requested_capability is None:
            return {
                "success": True,
                "capabilities": available,
            }

        requested = (
            self._normalize(requested_capability)
            .lower()
        )

        return {
            "success": requested in available,
            "requested": requested,
            "capabilities": available,
        }

    def find_capable(self, capability):
        capability = self._normalize(capability).lower()

        results = []

        for record in self.inventory.all():
            if capability in self.capabilities_for(record):
                results.append(record)

        return results

    def supported_capabilities(self):
        capabilities = set()

        for record in self.inventory.all():
            capabilities.update(
                self.capabilities_for(record)
            )

        return sorted(capabilities)

    @staticmethod
    def _normalize(value):
        if value is None:
            return ""

        return str(value).strip()


if __name__ == "__main__":
    print("=" * 55)
    print("    MYX STEP 10.5 CAPABILITY RESOLVER TEST")
    print("=" * 55)

    from src.system.discovery_record import DiscoveryRecord

    inventory = GlobalInventory()

    chrome = DiscoveryRecord(
        name="Google Chrome",
        item_type="application",
        capabilities=[
            "open",
            "launch",
            "search",
        ],
    )

    pdf = DiscoveryRecord(
        name="Python Tutorial.pdf",
        item_type="file",
        capabilities=[
            "find",
            "locate",
            "open",
        ],
    )

    inventory.add_many([chrome, pdf])

    resolver = CapabilityResolver(inventory)

    print("\n[TEST 1] Resolver Initialization")

    test1 = resolver.inventory is inventory

    print(
        "Inventory connected:",
        test1
    )

    print(
        "INITIALIZATION TEST:",
        "PASS" if test1 else "FAIL"
    )

    print("\n[TEST 2] Capability Check")

    test2 = resolver.can(chrome, "open")

    print("Chrome open:", test2)

    print(
        "CAPABILITY CHECK TEST:",
        "PASS" if test2 else "FAIL"
    )

    print("\n[TEST 3] Capability Resolution")

    result = resolver.resolve(
        pdf,
        "open"
    )

    test3 = result["success"] is True

    print("Result:", result)

    print(
        "RESOLUTION TEST:",
        "PASS" if test3 else "FAIL"
    )

    print("\n[TEST 4] Find Capable Resources")

    capable = resolver.find_capable("open")

    test4 = len(capable) == 2

    print(
        "Open-capable:",
        [item.name for item in capable]
    )

    print(
        "CAPABLE RESOURCE TEST:",
        "PASS" if test4 else "FAIL"
    )

    print("\n[TEST 5] Supported Capabilities")

    supported = resolver.supported_capabilities()

    test5 = (
        "open" in supported
        and "search" in supported
        and "find" in supported
    )

    print("Supported:", supported)

    print(
        "SUPPORTED CAPABILITY TEST:",
        "PASS" if test5 else "FAIL"
    )

    tests = [test1, test2, test3, test4, test5]
    passed = sum(tests)

    print("\n" + "-" * 55)
    print(f"Tests passed : {passed}/5")

    if passed == 5:
        print("CAPABILITY RESOLVER TEST: PASS")
        print("STEP 10.5 TEST PASSED")
    else:
        print("CAPABILITY RESOLVER TEST: FAIL")
        print("STEP 10.5 TEST FAILED")

    print("-" * 55)
    
