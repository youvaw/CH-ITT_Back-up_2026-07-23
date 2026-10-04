import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.storage.file_action_resolver import FileActionResolver
from src.system.storage.file_open_executor import FileOpenExecutor


class FileActionExecutor:
    """
    MYX STEP 9.12

    Connects:

        Natural Language
              â†“
        FileActionResolver
              â†“
        FileOpenExecutor

    Supported:
        find
        search
        locate
        show
        open

    Important:
        Only "open" performs execution.

        find/search/locate/show
        only return search results.
    """

    def __init__(self):
        self.resolver = FileActionResolver()
        self.open_executor = FileOpenExecutor()

        print("[FileActionExecutor] Initialized")

    # ---------------------------------------------------------
    # EXECUTE COMMAND
    # ---------------------------------------------------------

    def execute(self, command):
        if command is None:
            return {
                "success": False,
                "action": None,
                "query": "",
                "results": [],
                "count": 0,
                "message": "No command supplied."
            }

        command = str(command).strip()

        if not command:
            return {
                "success": False,
                "action": None,
                "query": "",
                "results": [],
                "count": 0,
                "message": "Empty command."
            }

        # Resolve natural language command
        resolved = self.resolver.resolve(command)

        if not resolved.get("success"):
            return resolved

        action = resolved.get("action")
        query = resolved.get("query")
        results = resolved.get("results", [])

        # -----------------------------------------------------
        # SEARCH-ONLY ACTIONS
        # -----------------------------------------------------

        if action in ("find", "search", "locate", "show"):
            return {
                "success": True,
                "action": action,
                "query": query,
                "results": results,
                "count": len(results),
                "execution": "search_only",
                "message": f"Found {len(results)} result(s)."
            }

        # -----------------------------------------------------
        # OPEN ACTION
        # -----------------------------------------------------

        if action == "open":

            if not results:
                return {
                    "success": False,
                    "action": "open",
                    "query": query,
                    "results": [],
                    "count": 0,
                    "execution": "not_executed",
                    "message": "No matching file found."
                }

            open_result = self.open_executor.execute(results)

            return {
                "success": open_result.get("success", False),
                "action": "open",
                "query": query,
                "results": results,
                "count": len(results),
                "selected": open_result.get("selected"),
                "candidates": open_result.get("candidates", []),
                "needs_selection": open_result.get(
                    "needs_selection",
                    False
                ),
                "execution": (
                    "executed"
                    if open_result.get("success")
                    else "not_executed"
                ),
                "message": open_result.get(
                    "message",
                    "Open operation completed."
                )
            }

        return {
            "success": False,
            "action": action,
            "query": query,
            "results": results,
            "count": len(results),
            "message": "Unsupported file action."
        }


# =============================================================
# STEP 9.12 TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 45)
    print("    MYX STEP 9.12 FILE ACTION TEST")
    print("=" * 45)

    executor = FileActionExecutor()

    tests_passed = 0
    total_tests = 5

    # ---------------------------------------------------------
    # TEST 1 â€” FIND
    # ---------------------------------------------------------

    print("\n[TEST 1] Find Command")

    result = executor.execute("find app")

    print("Success :", result["success"])
    print("Action  :", result["action"])
    print("Query   :", result["query"])
    print("Results :", result["count"])

    if (
        result["success"]
        and result["action"] == "find"
        and result["query"] == "app"
    ):
        print("FIND COMMAND TEST: PASS")
        tests_passed += 1
    else:
        print("FIND COMMAND TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 2 â€” SEARCH
    # ---------------------------------------------------------

    print("\n[TEST 2] Search Command")

    result = executor.execute("search app")

    print("Success :", result["success"])
    print("Action  :", result["action"])
    print("Execution:", result.get("execution"))

    if (
        result["success"]
        and result["action"] == "search"
        and result["execution"] == "search_only"
    ):
        print("SEARCH COMMAND TEST: PASS")
        tests_passed += 1
    else:
        print("SEARCH COMMAND TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 3 â€” LOCATE
    # ---------------------------------------------------------

    print("\n[TEST 3] Locate Command")

    result = executor.execute("where is app")

    print("Success :", result["success"])
    print("Action  :", result["action"])
    print("Query   :", result["query"])

    if (
        result["success"]
        and result["action"] == "locate"
    ):
        print("LOCATE COMMAND TEST: PASS")
        tests_passed += 1
    else:
        print("LOCATE COMMAND TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 4 â€” OPEN WITH NO MATCH
    # ---------------------------------------------------------

    print("\n[TEST 4] Open Unknown File")

    result = executor.execute(
        "open xyz_file_that_does_not_exist_999999"
    )

    print("Success :", result["success"])
    print("Action  :", result["action"])
    print("Execution:", result.get("execution"))
    print("Message :", result["message"])

    if (
        result["action"] == "open"
        and not result["success"]
        and result["execution"] == "not_executed"
    ):
        print("SAFE UNKNOWN OPEN TEST: PASS")
        tests_passed += 1
    else:
        print("SAFE UNKNOWN OPEN TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 5 â€” OPEN EXISTING PROJECT FILE
    # ---------------------------------------------------------

    print("\n[TEST 5] Open Existing File Resolution")

    test_file = os.path.join(
        PROJECT_ROOT,
        "src",
        "system",
        "file_action_resolver.py"
    )

    # Directly test the integration without actually
    # launching Windows application.
    selection = executor.open_executor.select_candidate(
        [
            {
                "name": "file_action_resolver.py",
                "path": test_file
            }
        ]
    )

    print("Success :", selection["success"])
    print("Selected:", selection["selected"])

    if (
        selection["success"]
        and selection["selected"] == os.path.abspath(test_file)
    ):
        print("OPEN RESOLUTION TEST: PASS")
        tests_passed += 1
    else:
        print("OPEN RESOLUTION TEST: FAIL")

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    print("\n" + "-" * 45)
    print(f"Tests passed : {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("FILE ACTION EXECUTOR TEST: PASS")
        print("STEP 9.12 TEST PASSED")
    else:
        print("FILE ACTION EXECUTOR TEST: FAIL")

    print("-" * 45)
    

