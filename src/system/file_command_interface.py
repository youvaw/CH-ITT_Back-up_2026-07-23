import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.file_operation_controller import FileOperationController


class FileCommandInterface:
    """
    MYX File Command Interface

    Provides a clean public interface between the
    higher-level MYX system and the file subsystem.

    Higher-level system should eventually call:

        interface.execute(command)

    instead of knowing about:
        Resolver
        Search
        Executor
        Selection
        Formatter
    """

    def __init__(self, controller=None):
        self.controller = controller or FileOperationController()

        print("[FileCommandInterface] Initialized")

    # -----------------------------------------------------
    # MAIN COMMAND API
    # -----------------------------------------------------

    def execute(self, command):
        command = self._normalize(command)

        if not command:
            return {
                "success": False,
                "handled": False,
                "action": None,
                "query": "",
                "response": (
                    "Please tell me which file you want me to work with."
                ),
            }

        try:
            result = self.controller.execute(command)

            result["handled"] = True

            return result

        except Exception as error:
            print(
                f"[FileCommandInterface] Error: {error}"
            )

            return {
                "success": False,
                "handled": True,
                "action": None,
                "query": command,
                "response": (
                    f"I couldn't complete the file operation: {error}"
                ),
            }

    # -----------------------------------------------------
    # SIMPLE RESPONSE
    # -----------------------------------------------------

    def process(self, command):
        result = self.execute(command)

        return result.get(
            "response",
            "I couldn't complete the file operation."
        )

    # -----------------------------------------------------
    # FILE COMMAND DETECTION
    # -----------------------------------------------------

    def can_handle(self, command):
        command = self._normalize(command)

        if not command:
            return False

        try:
            return self.controller.is_file_command(command)
        except Exception as error:
            print(
                f"[FileCommandInterface] Detection error: {error}"
            )
            return False

    # -----------------------------------------------------
    # ACTION RESOLUTION
    # -----------------------------------------------------

    def resolve(self, command):
        command = self._normalize(command)

        if not command:
            return None

        try:
            return self.controller.resolve_action(command)
        except Exception as error:
            print(
                f"[FileCommandInterface] Resolve error: {error}"
            )
            return None

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
    print("    MYX STEP 9.17 FILE COMMAND INTERFACE TEST")
    print("=" * 50)

    interface = FileCommandInterface()

    passed = 0
    total = 5

    # -----------------------------------------------------
    # TEST 1
    # -----------------------------------------------------

    print("\n[TEST 1] Interface Initialization")

    if interface.controller is not None:
        print("Controller connected: PASS")
        passed += 1
    else:
        print("Controller connected: FAIL")

    # -----------------------------------------------------
    # TEST 2
    # -----------------------------------------------------

    print("\n[TEST 2] Empty Command Safety")

    result = interface.execute("")

    print(f"Handled: {result.get('handled')}")
    print(f"Success: {result.get('success')}")
    print(f"Response: {result.get('response')}")

    if (
        result.get("handled") is False
        and result.get("success") is False
        and result.get("response")
    ):
        print("EMPTY COMMAND TEST: PASS")
        passed += 1
    else:
        print("EMPTY COMMAND TEST: FAIL")

    # -----------------------------------------------------
    # TEST 3
    # -----------------------------------------------------

    print("\n[TEST 3] File Command Detection")

    detected = interface.can_handle(
        "find python"
    )

    print(f"Detected: {detected}")

    if detected is True:
        print("COMMAND DETECTION TEST: PASS")
        passed += 1
    else:
        print("COMMAND DETECTION TEST: FAIL")

    # -----------------------------------------------------
    # TEST 4
    # -----------------------------------------------------

    print("\n[TEST 4] Action Resolution")

    result = interface.resolve(
        "find python"
    )

    print(f"Resolved: {result}")

    if isinstance(result, dict):
        print("ACTION RESOLUTION TEST: PASS")
        passed += 1
    else:
        print("ACTION RESOLUTION TEST: FAIL")

    # -----------------------------------------------------
    # TEST 5
    # -----------------------------------------------------

    print("\n[TEST 5] Public Process API")

    response = interface.process(
        "find python"
    )

    print(f"Response: {response}")

    if isinstance(response, str) and response.strip():
        print("PUBLIC PROCESS API TEST: PASS")
        passed += 1
    else:
        print("PUBLIC PROCESS API TEST: FAIL")

    # -----------------------------------------------------
    # FINAL
    # -----------------------------------------------------

    print("\n" + "-" * 50)
    print(f"Tests passed : {passed}/{total}")

    if passed == total:
        print("FILE COMMAND INTERFACE TEST: PASS")
        print("STEP 9.17 TEST PASSED")
    else:
        print("FILE COMMAND INTERFACE TEST: FAIL")
        print("STEP 9.17 TEST FAILED")

    print("-" * 50)


if __name__ == "__main__":
    run_tests()
