import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.file_command_interface import FileCommandInterface
from src.system.file_capability_registry import FileCapabilityRegistry


class FileSystemService:
    """
    MYX File System Service

    High-level file subsystem.

    Responsibilities:

        Capability discovery
              +
        File command interface
              =
        Unified File Service
    """

    def __init__(
        self,
        command_interface=None,
        capability_registry=None
    ):

        self.command_interface = (
            command_interface
            or FileCommandInterface()
        )

        self.capability_registry = (
            capability_registry
            or FileCapabilityRegistry()
        )

        print("[FileSystemService] Initialized")

    # -----------------------------------------------------
    # COMMAND
    # -----------------------------------------------------

    def execute(self, command):

        return self.command_interface.execute(
            command
        )

    # -----------------------------------------------------
    # SIMPLE PROCESS
    # -----------------------------------------------------

    def process(self, command):

        return self.command_interface.process(
            command
        )

    # -----------------------------------------------------
    # CAN HANDLE
    # -----------------------------------------------------

    def can_handle(self, command):

        return self.command_interface.can_handle(
            command
        )

    # -----------------------------------------------------
    # CAPABILITIES
    # -----------------------------------------------------

    def capabilities(self):

        return self.capability_registry.list()

    # -----------------------------------------------------
    # CAPABILITY CHECK
    # -----------------------------------------------------

    def has_capability(self, capability):

        return self.capability_registry.has(
            capability
        )

    # -----------------------------------------------------
    # SYSTEM STATUS
    # -----------------------------------------------------

    def status(self):

        capabilities = self.capabilities()

        return {
            "service": "file_system",
            "ready": True,
            "capability_count": len(capabilities),
            "capabilities": capabilities,
        }

    # -----------------------------------------------------
    # NORMALIZATION
    # -----------------------------------------------------

    def _normalize(self, value):

        if value is None:
            return ""

        return str(value).strip()


# =========================================================
# TESTS
# =========================================================

def run_tests():

    print("=" * 50)
    print("    MYX STEP 9.19 FILE SYSTEM SERVICE TEST")
    print("=" * 50)

    service = FileSystemService()

    passed = 0
    total = 5

    # -----------------------------------------------------
    # TEST 1
    # -----------------------------------------------------

    print("\n[TEST 1] Service Initialization")

    if (
        service.command_interface is not None
        and service.capability_registry is not None
    ):
        print("Service components ready: PASS")
        passed += 1
    else:
        print("Service components ready: FAIL")

    # -----------------------------------------------------
    # TEST 2
    # -----------------------------------------------------

    print("\n[TEST 2] Capability Discovery")

    capabilities = service.capabilities()

    print(
        f"Capabilities discovered: {len(capabilities)}"
    )

    for capability in capabilities:
        print(f"  - {capability}")

    if len(capabilities) >= 5:
        print("CAPABILITY DISCOVERY TEST: PASS")
        passed += 1
    else:
        print("CAPABILITY DISCOVERY TEST: FAIL")

    # -----------------------------------------------------
    # TEST 3
    # -----------------------------------------------------

    print("\n[TEST 3] Capability Check")

    result = service.has_capability("open")

    print(f"Open capability: {result}")

    if result is True:
        print("CAPABILITY CHECK TEST: PASS")
        passed += 1
    else:
        print("CAPABILITY CHECK TEST: FAIL")

    # -----------------------------------------------------
    # TEST 4
    # -----------------------------------------------------

    print("\n[TEST 4] File Command Handling")

    result = service.execute(
        "find python"
    )

    print(
        f"Handled: {result.get('handled')}"
    )

    print(
        f"Response: {result.get('response')}"
    )

    if (
        result.get("handled") is True
        and result.get("response")
    ):
        print("COMMAND HANDLING TEST: PASS")
        passed += 1
    else:
        print("COMMAND HANDLING TEST: FAIL")

    # -----------------------------------------------------
    # TEST 5
    # -----------------------------------------------------

    print("\n[TEST 5] Service Status")

    status = service.status()

    print(f"Status: {status}")

    if (
        status.get("service") == "file_system"
        and status.get("ready") is True
        and status.get("capability_count", 0) >= 5
    ):
        print("SERVICE STATUS TEST: PASS")
        passed += 1
    else:
        print("SERVICE STATUS TEST: FAIL")

    # -----------------------------------------------------
    # FINAL
    # -----------------------------------------------------

    print("\n" + "-" * 50)
    print(f"Tests passed : {passed}/{total}")

    if passed == total:
        print("FILE SYSTEM SERVICE TEST: PASS")
        print("STEP 9.19 TEST PASSED")
    else:
        print("FILE SYSTEM SERVICE TEST: FAIL")
        print("STEP 9.19 TEST FAILED")

    print("-" * 50)


if __name__ == "__main__":
    run_tests()
    
