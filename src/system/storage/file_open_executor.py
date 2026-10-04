import os
import sys
import traceback

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class FileOpenExecutor:
    """
    MYX STEP 9.11

    Safely opens a file resolved by the file-search system.

    Rules:
        1. File must exist.
        2. File must be a regular file.
        3. Exactly ONE candidate -> open.
        4. Multiple candidates -> do NOT open; request selection.
        5. Zero candidates -> fail safely.

    Destructive operations are NOT supported.
    """

    def __init__(self):
        print("[FileOpenExecutor] Initialized")

    # ---------------------------------------------------------
    # PATH VALIDATION
    # ---------------------------------------------------------

    def normalize_path(self, path):
        if path is None:
            return ""

        return os.path.abspath(
            os.path.expandvars(
                os.path.expanduser(
                    str(path).strip()
                )
            )
        )

    def validate_file(self, path):
        path = self.normalize_path(path)

        if not path:
            return {
                "valid": False,
                "path": "",
                "reason": "Empty file path."
            }

        if not os.path.exists(path):
            return {
                "valid": False,
                "path": path,
                "reason": "File does not exist."
            }

        if not os.path.isfile(path):
            return {
                "valid": False,
                "path": path,
                "reason": "Path is not a regular file."
            }

        return {
            "valid": True,
            "path": path,
            "reason": "Valid file."
        }

    # ---------------------------------------------------------
    # EXTRACT PATHS FROM SEARCH RESULTS
    # ---------------------------------------------------------

    def extract_paths(self, results):
        paths = []

        if not results:
            return paths

        for result in results:
            path = None

            if isinstance(result, str):
                path = result

            elif isinstance(result, dict):
                path = (
                    result.get("path")
                    or result.get("full_path")
                    or result.get("file_path")
                )

            else:
                path = getattr(result, "path", None)

            if not path:
                continue

            path = self.normalize_path(path)

            if path not in paths:
                paths.append(path)

        return paths

    # ---------------------------------------------------------
    # SAFE CANDIDATE SELECTION
    # ---------------------------------------------------------

    def select_candidate(self, results):
        paths = self.extract_paths(results)

        valid_paths = []

        for path in paths:
            validation = self.validate_file(path)

            if validation["valid"]:
                valid_paths.append(path)

        if not valid_paths:
            return {
                "success": False,
                "selected": None,
                "candidates": [],
                "count": 0,
                "needs_selection": False,
                "message": "No valid file candidate found."
            }

        if len(valid_paths) > 1:
            return {
                "success": False,
                "selected": None,
                "candidates": valid_paths,
                "count": len(valid_paths),
                "needs_selection": True,
                "message": (
                    f"Multiple files found ({len(valid_paths)}). "
                    "Selection required."
                )
            }

        return {
            "success": True,
            "selected": valid_paths[0],
            "candidates": valid_paths,
            "count": 1,
            "needs_selection": False,
            "message": "One valid file selected."
        }

    # ---------------------------------------------------------
    # OPEN FILE
    # ---------------------------------------------------------

    def open_file(self, path):
        validation = self.validate_file(path)

        if not validation["valid"]:
            return {
                "success": False,
                "path": validation["path"],
                "message": validation["reason"]
            }

        try:
            os.startfile(validation["path"])

            return {
                "success": True,
                "path": validation["path"],
                "message": f"Opening {os.path.basename(validation['path'])}."
            }

        except Exception as e:
            return {
                "success": False,
                "path": validation["path"],
                "message": f"Unable to open file: {e}"
            }

    # ---------------------------------------------------------
    # EXECUTE SEARCH RESULT
    # ---------------------------------------------------------

    def execute(self, results):
        selection = self.select_candidate(results)

        if not selection["success"]:
            return selection

        return self.open_file(selection["selected"])


# =============================================================
# STEP 9.11 TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 42)
    print("    MYX STEP 9.11 FILE OPEN TEST")
    print("=" * 42)

    executor = FileOpenExecutor()

    tests_passed = 0
    total_tests = 4

    # ---------------------------------------------------------
    # TEST 1 — VALID FILE
    # ---------------------------------------------------------

    print("\n[TEST 1] Valid File")

    test_file = os.path.join(
        PROJECT_ROOT,
        "src",
        "system",
        "file_action_resolver.py"
    )

    result = executor.validate_file(test_file)

    print("Valid :", result["valid"])
    print("Path  :", result["path"])

    if result["valid"]:
        print("VALID FILE TEST: PASS")
        tests_passed += 1
    else:
        print("VALID FILE TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 2 — INVALID FILE
    # ---------------------------------------------------------

    print("\n[TEST 2] Invalid File")

    fake_file = os.path.join(
        PROJECT_ROOT,
        "this_file_does_not_exist_999.py"
    )

    result = executor.validate_file(fake_file)

    print("Valid :", result["valid"])
    print("Reason:", result["reason"])

    if not result["valid"]:
        print("INVALID FILE TEST: PASS")
        tests_passed += 1
    else:
        print("INVALID FILE TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 3 — SINGLE CANDIDATE
    # ---------------------------------------------------------

    print("\n[TEST 3] Single Candidate Selection")

    result = executor.select_candidate(
        [
            {
                "name": "file_action_resolver.py",
                "path": test_file
            }
        ]
    )

    print("Success :", result["success"])
    print("Selected:", result["selected"])

    if result["success"] and result["count"] == 1:
        print("SINGLE CANDIDATE TEST: PASS")
        tests_passed += 1
    else:
        print("SINGLE CANDIDATE TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 4 — MULTIPLE CANDIDATES
    # ---------------------------------------------------------

    print("\n[TEST 4] Multiple Candidates Safety")

    result = executor.select_candidate(
        [
            {
                "name": "file_action_resolver.py",
                "path": test_file
            },
            {
                "name": "file_open_executor.py",
                "path": os.path.join(
                    PROJECT_ROOT,
                    "src",
                    "system",
                    "file_open_executor.py"
                )
            }
        ]
    )

    print("Success         :", result["success"])
    print("Candidates     :", result["count"])
    print("Needs selection:", result["needs_selection"])

    if (
        not result["success"]
        and result["needs_selection"]
        and result["count"] >= 2
    ):
        print("MULTIPLE CANDIDATE SAFETY TEST: PASS")
        tests_passed += 1
    else:
        print("MULTIPLE CANDIDATE SAFETY TEST: FAIL")

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    print("\n" + "-" * 42)
    print(f"Tests passed : {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("FILE OPEN EXECUTOR TEST: PASS")
        print("STEP 9.11 TEST PASSED")
    else:
        print("FILE OPEN EXECUTOR TEST: FAIL")

    print("-" * 42)
    
