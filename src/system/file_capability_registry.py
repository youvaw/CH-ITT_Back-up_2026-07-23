import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class FileCapabilityRegistry:
    """
    MYX File Capability Registry

    Describes generic file capabilities.

    This is NOT a list of individual files.

    It describes what MYX can do with files.
    """

    def __init__(self):

        self.capabilities = {
            "find": {
                "name": "Find Files",
                "description": (
                    "Find files by name or search query."
                ),
                "enabled": True,
            },

            "search": {
                "name": "Search Files",
                "description": (
                    "Search indexed files."
                ),
                "enabled": True,
            },

            "locate": {
                "name": "Locate Files",
                "description": (
                    "Locate files and report their paths."
                ),
                "enabled": True,
            },

            "show": {
                "name": "Show Files",
                "description": (
                    "Show matching files."
                ),
                "enabled": True,
            },

            "open": {
                "name": "Open Files",
                "description": (
                    "Open a selected file."
                ),
                "enabled": True,
            },

            "select": {
                "name": "Select File",
                "description": (
                    "Select between multiple matching files."
                ),
                "enabled": True,
            },
        }

        print("[FileCapabilityRegistry] Initialized")

    # -----------------------------------------------------
    # CAPABILITY CHECK
    # -----------------------------------------------------

    def has(self, capability):
        capability = self._normalize(capability)

        if capability not in self.capabilities:
            return False

        return self.capabilities[capability].get(
            "enabled",
            False
        )

    # -----------------------------------------------------
    # GET CAPABILITY
    # -----------------------------------------------------

    def get(self, capability):
        capability = self._normalize(capability)

        return self.capabilities.get(capability)

    # -----------------------------------------------------
    # LIST CAPABILITIES
    # -----------------------------------------------------

    def list(self):
        return [
            key
            for key, value in self.capabilities.items()
            if value.get("enabled", False)
        ]

    # -----------------------------------------------------
    # COUNT
    # -----------------------------------------------------

    def count(self):
        return len(self.list())

    # -----------------------------------------------------
    # DESCRIPTION
    # -----------------------------------------------------

    def describe(self, capability):
        data = self.get(capability)

        if not data:
            return None

        return data.get("description")

    # -----------------------------------------------------
    # REPORT
    # -----------------------------------------------------

    def report(self):

        return {
            "total": self.count(),
            "capabilities": self.list(),
        }

    # -----------------------------------------------------
    # NORMALIZATION
    # -----------------------------------------------------

    def _normalize(self, value):

        if value is None:
            return ""

        return str(value).strip().lower()


# =========================================================
# TESTS
# =========================================================

def run_tests():

    print("=" * 50)
    print("    MYX STEP 9.18 CAPABILITY REGISTRY TEST")
    print("=" * 50)

    registry = FileCapabilityRegistry()

    passed = 0
    total = 5

    # -----------------------------------------------------
    # TEST 1
    # -----------------------------------------------------

    print("\n[TEST 1] Registry Initialization")

    if registry.count() > 0:
        print(
            f"Capabilities discovered: {registry.count()}"
        )
        print("INITIALIZATION TEST: PASS")
        passed += 1
    else:
        print("INITIALIZATION TEST: FAIL")

    # -----------------------------------------------------
    # TEST 2
    # -----------------------------------------------------

    print("\n[TEST 2] Find Capability")

    result = registry.has("find")

    print(f"Find enabled: {result}")

    if result is True:
        print("FIND CAPABILITY TEST: PASS")
        passed += 1
    else:
        print("FIND CAPABILITY TEST: FAIL")

    # -----------------------------------------------------
    # TEST 3
    # -----------------------------------------------------

    print("\n[TEST 3] Open Capability")

    result = registry.has("open")

    print(f"Open enabled: {result}")

    if result is True:
        print("OPEN CAPABILITY TEST: PASS")
        passed += 1
    else:
        print("OPEN CAPABILITY TEST: FAIL")

    # -----------------------------------------------------
    # TEST 4
    # -----------------------------------------------------

    print("\n[TEST 4] Capability Listing")

    capabilities = registry.list()

    print("Capabilities:")

    for capability in capabilities:
        print(f"  - {capability}")

    if len(capabilities) >= 5:
        print("LIST TEST: PASS")
        passed += 1
    else:
        print("LIST TEST: FAIL")

    # -----------------------------------------------------
    # TEST 5
    # -----------------------------------------------------

    print("\n[TEST 5] Unknown Capability Safety")

    result = registry.has(
        "unknown_capability"
    )

    print(f"Unknown capability: {result}")

    if result is False:
        print("UNKNOWN CAPABILITY TEST: PASS")
        passed += 1
    else:
        print("UNKNOWN CAPABILITY TEST: FAIL")

    # -----------------------------------------------------
    # FINAL
    # -----------------------------------------------------

    print("\n" + "-" * 50)
    print(f"Tests passed : {passed}/{total}")

    if passed == total:
        print("FILE CAPABILITY REGISTRY TEST: PASS")
        print("STEP 9.18 TEST PASSED")
    else:
        print("FILE CAPABILITY REGISTRY TEST: FAIL")
        print("STEP 9.18 TEST FAILED")

    print("-" * 50)


if __name__ == "__main__":
    run_tests()
    
