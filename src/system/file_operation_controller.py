import os
import sys

# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------
# IMPORT EXISTING FILE SYSTEM MODULES
# ---------------------------------------------------------

from src.system.storage.file_action_resolver import FileActionResolver
from src.system.storage.file_action_executor import FileActionExecutor
from src.system.storage.file_response_formatter import FileResponseFormatter


# ---------------------------------------------------------
# FILE OPERATION CONTROLLER
# ---------------------------------------------------------

class FileOperationController:
    """
    MYX File Operation Controller

    Central coordinator for file-related commands.

    Pipeline:

        User Command
             â†“
        Action Resolver
             â†“
        File Action Executor
             â†“
        Selection / Open / Search
             â†“
        Response Formatter
             â†“
        Human-readable response
    """

    def __init__(
        self,
        resolver=None,
        executor=None,
        formatter=None
    ):
        self.resolver = resolver or FileActionResolver()
        self.executor = executor or FileActionExecutor()
        self.formatter = formatter or FileResponseFormatter()

        print("[FileOperationController] Initialized")

    # -----------------------------------------------------
    # COMMAND EXECUTION
    # -----------------------------------------------------

    def execute(self, command):
        """
        Execute a complete file-related command.

        Returns a structured result plus formatted response.
        """

        command = self._normalize(command)

        if not command:
            return {
                "success": False,
                "action": None,
                "query": "",
                "response": "Please tell me which file you want me to work with."
            }

        try:
            result = self.executor.execute(command)

        except Exception as error:
            print(
                f"[FileOperationController] Execution error: {error}"
            )

            result = {
                "success": False,
                "action": None,
                "query": command,
                "message": (
                    f"I couldn't complete the file operation: {error}"
                )
            }

        response = self.formatter.format(result)

        result["response"] = response

        return result

    # -----------------------------------------------------
    # SIMPLE RESPONSE API
    # -----------------------------------------------------

    def process(self, command):
        """
        Execute command and return only the human-readable response.
        """

        result = self.execute(command)

        return result.get(
            "response",
            "I couldn't complete the file operation."
        )

    # -----------------------------------------------------
    # ACTION INSPECTION
    # -----------------------------------------------------

    def resolve_action(self, command):
        """
        Resolve the action without executing it.

        Useful for future Brain / Router integration.
        """

        command = self._normalize(command)

        if not command:
            return None

        try:
            return self.resolver.resolve(command)
        except Exception as error:
            print(
                f"[FileOperationController] Resolve error: {error}"
            )
            return None

    # -----------------------------------------------------
    # COMMAND CHECK
    # -----------------------------------------------------

    def is_file_command(self, command):
        """
        Determine whether the command appears to be
        a file operation.
        """

        command = self._normalize(command)

        if not command:
            return False

        try:
            action = self.resolve_action(command)
            return action is not None
        except Exception:
            return False

    # -----------------------------------------------------
    # NORMALIZATION
    # -----------------------------------------------------

    def _normalize(self, value):
        if value is None:
            return ""

        return str(value).strip()


# ---------------------------------------------------------
# TESTS
# ---------------------------------------------------------

def run_tests():

    print("=" * 48)
    print("    MYX STEP 9.16 FILE OPERATION TEST")
    print("=" * 48)

    controller = FileOperationController()

    passed = 0
    total = 5

    # -----------------------------------------------------
    # TEST 1 â€” Initialization
    # -----------------------------------------------------

    print("\n[TEST 1] Controller Initialization")

    if (
        controller.resolver is not None
        and controller.executor is not None
        and controller.formatter is not None
    ):
        print("Controller components ready: PASS")
        passed += 1
    else:
        print("Controller components ready: FAIL")

    # -----------------------------------------------------
    # TEST 2 â€” Empty Command Safety
    # -----------------------------------------------------

    print("\n[TEST 2] Empty Command Safety")

    result = controller.execute("")

    if (
        result.get("success") is False
        and result.get("response")
    ):
        print(
            f"Response: {result.get('response')}"
        )
        print("EMPTY COMMAND TEST: PASS")
        passed += 1
    else:
        print("EMPTY COMMAND TEST: FAIL")

    # -----------------------------------------------------
    # TEST 3 â€” Action Resolution
    # -----------------------------------------------------

    print("\n[TEST 3] Action Resolution")

    action = controller.resolve_action(
        "find file_action_resolver.py"
    )

    print(f"Resolved action: {action}")

    if action:
        print("ACTION RESOLUTION TEST: PASS")
        passed += 1
    else:
        print("ACTION RESOLUTION TEST: FAIL")

    # -----------------------------------------------------
    # TEST 4 â€” File Search Pipeline
    # -----------------------------------------------------

    print("\n[TEST 4] File Search Pipeline")

    result = controller.execute(
        "find file_action_resolver.py"
    )

    response = result.get("response", "")

    print(f"Response: {response}")

    if (
        result.get("success") is True
        and "file_action_resolver.py" in response.lower()
    ):
        print("FILE SEARCH PIPELINE TEST: PASS")
        passed += 1
    else:
        print("FILE SEARCH PIPELINE TEST: FAIL")

    # -----------------------------------------------------
    # TEST 5 â€” Multiple Candidate Response
    # -----------------------------------------------------

    print("\n[TEST 5] Multiple Candidate Handling")

    multiple_result = {
        "success": False,
        "action": "open",
        "query": "python",
        "needs_selection": True,
        "candidates": [
            {
                "path": os.path.join(
                    PROJECT_ROOT,
                    "src",
                    "system",
                    "file_action_resolver.py"
                )
            },
            {
                "path": os.path.join(
                    PROJECT_ROOT,
                    "src",
                    "system",
                    "file_open_executor.py"
                )
            }
        ]
    }

    response = controller.formatter.format(
        multiple_result
    )

    print("Response:")
    print(response)

    response_lower = response.lower()

    if (
        "multiple" in response_lower
        and "1." in response
        and "2." in response
        and "file_action_resolver.py" in response_lower
        and "file_open_executor.py" in response_lower
    ):
        print("MULTIPLE CANDIDATE TEST: PASS")
        passed += 1
    else:
        print("MULTIPLE CANDIDATE TEST: FAIL")

    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    print("\n" + "-" * 48)
    print(f"Tests passed : {passed}/{total}")

    if passed == total:
        print("FILE OPERATION CONTROLLER TEST: PASS")
        print("STEP 9.16 TEST PASSED")
    else:
        print("FILE OPERATION CONTROLLER TEST: FAIL")
        print("STEP 9.16 TEST FAILED")

    print("-" * 48)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":
    run_tests()
    

