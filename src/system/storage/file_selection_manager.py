import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class FileSelectionManager:
    """
    MYX STEP 9.13

    Handles multiple file candidates safely.

    Rules:

        0 candidates
            -> no match

        1 candidate
            -> automatic selection

        2+ candidates
            -> selection required

    This module does NOT open files.

    It only decides which candidate is safe
    to pass to the execution layer.
    """

    def __init__(self):
        print("[FileSelectionManager] Initialized")

    # ---------------------------------------------------------
    # NORMALIZATION
    # ---------------------------------------------------------

    def normalize_path(self, path):
        if not path:
            return ""

        return os.path.abspath(
            os.path.expandvars(
                os.path.expanduser(
                    str(path).strip()
                )
            )
        )

    # ---------------------------------------------------------
    # EXTRACT CANDIDATES
    # ---------------------------------------------------------

    def extract_candidates(self, results):

        candidates = []

        if not results:
            return candidates

        for result in results:

            path = None
            name = None

            if isinstance(result, str):
                path = result

            elif isinstance(result, dict):
                path = (
                    result.get("path")
                    or result.get("full_path")
                    or result.get("file_path")
                )

                name = (
                    result.get("name")
                    or result.get("filename")
                )

            else:
                path = getattr(result, "path", None)
                name = getattr(result, "name", None)

            if not path:
                continue

            path = self.normalize_path(path)

            if not os.path.exists(path):
                continue

            if path in [
                item["path"]
                for item in candidates
            ]:
                continue

            candidates.append({
                "name": name or os.path.basename(path),
                "path": path,
                "exists": True,
                "is_file": os.path.isfile(path),
                "is_directory": os.path.isdir(path)
            })

        return candidates

    # ---------------------------------------------------------
    # SELECT
    # ---------------------------------------------------------

    def select(self, results):

        candidates = self.extract_candidates(results)

        if not candidates:
            return {
                "success": False,
                "selected": None,
                "candidates": [],
                "count": 0,
                "needs_selection": False,
                "message": "No valid candidates found."
            }

        # Exactly one candidate
        if len(candidates) == 1:

            return {
                "success": True,
                "selected": candidates[0],
                "candidates": candidates,
                "count": 1,
                "needs_selection": False,
                "message": "One candidate selected."
            }

        # Multiple candidates
        return {
            "success": False,
            "selected": None,
            "candidates": candidates,
            "count": len(candidates),
            "needs_selection": True,
            "message": (
                f"{len(candidates)} candidates found. "
                "User selection required."
            )
        }

    # ---------------------------------------------------------
    # GET DISPLAY OPTIONS
    # ---------------------------------------------------------

    def get_options(self, results):

        selection = self.select(results)

        options = []

        for index, candidate in enumerate(
            selection["candidates"],
            start=1
        ):
            options.append({
                "number": index,
                "name": candidate["name"],
                "path": candidate["path"],
                "type": (
                    "file"
                    if candidate["is_file"]
                    else "directory"
                    if candidate["is_directory"]
                    else "other"
                )
            })

        return {
            "success": selection["success"],
            "needs_selection": selection["needs_selection"],
            "count": selection["count"],
            "selected": selection["selected"],
            "options": options,
            "message": selection["message"]
        }

    # ---------------------------------------------------------
    # SELECT BY NUMBER
    # ---------------------------------------------------------

    def select_number(self, results, number):

        selection = self.select(results)

        candidates = selection["candidates"]

        try:
            number = int(number)
        except (TypeError, ValueError):
            return {
                "success": False,
                "selected": None,
                "message": "Invalid selection number."
            }

        index = number - 1

        if index < 0 or index >= len(candidates):
            return {
                "success": False,
                "selected": None,
                "message": "Selection number is out of range."
            }

        selected = candidates[index]

        return {
            "success": True,
            "selected": selected,
            "message": f"Selected {selected['name']}."
        }


# =============================================================
# STEP 9.13 TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 45)
    print("    MYX STEP 9.13 FILE SELECTION TEST")
    print("=" * 45)

    manager = FileSelectionManager()

    tests_passed = 0
    total_tests = 5

    test_file_1 = os.path.join(
        PROJECT_ROOT,
        "src",
        "system",
        "file_action_resolver.py"
    )

    test_file_2 = os.path.join(
        PROJECT_ROOT,
        "src",
        "system",
        "file_open_executor.py"
    )

    # ---------------------------------------------------------
    # TEST 1 — NO RESULTS
    # ---------------------------------------------------------

    print("\n[TEST 1] No Candidates")

    result = manager.select([])

    print("Success :", result["success"])
    print("Count   :", result["count"])

    if (
        not result["success"]
        and result["count"] == 0
    ):
        print("NO CANDIDATE TEST: PASS")
        tests_passed += 1
    else:
        print("NO CANDIDATE TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 2 — SINGLE CANDIDATE
    # ---------------------------------------------------------

    print("\n[TEST 2] Single Candidate")

    result = manager.select([
        {
            "name": "file_action_resolver.py",
            "path": test_file_1
        }
    ])

    print("Success :", result["success"])
    print("Selected:", result["selected"])

    if (
        result["success"]
        and result["count"] == 1
        and not result["needs_selection"]
    ):
        print("SINGLE CANDIDATE TEST: PASS")
        tests_passed += 1
    else:
        print("SINGLE CANDIDATE TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 3 — MULTIPLE CANDIDATES
    # ---------------------------------------------------------

    print("\n[TEST 3] Multiple Candidates")

    result = manager.select([
        {
            "name": "file_action_resolver.py",
            "path": test_file_1
        },
        {
            "name": "file_open_executor.py",
            "path": test_file_2
        }
    ])

    print("Success         :", result["success"])
    print("Count           :", result["count"])
    print("Needs selection :", result["needs_selection"])

    if (
        not result["success"]
        and result["count"] == 2
        and result["needs_selection"]
    ):
        print("MULTIPLE CANDIDATE TEST: PASS")
        tests_passed += 1
    else:
        print("MULTIPLE CANDIDATE TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 4 — OPTIONS
    # ---------------------------------------------------------

    print("\n[TEST 4] Candidate Options")

    result = manager.get_options([
        {
            "name": "file_action_resolver.py",
            "path": test_file_1
        },
        {
            "name": "file_open_executor.py",
            "path": test_file_2
        }
    ])

    print("Options:", result["options"])

    if (
        result["count"] == 2
        and len(result["options"]) == 2
        and result["options"][0]["number"] == 1
        and result["options"][1]["number"] == 2
    ):
        print("OPTIONS TEST: PASS")
        tests_passed += 1
    else:
        print("OPTIONS TEST: FAIL")

    # ---------------------------------------------------------
    # TEST 5 — NUMBER SELECTION
    # ---------------------------------------------------------

    print("\n[TEST 5] Number Selection")

    result = manager.select_number(
        [
            {
                "name": "file_action_resolver.py",
                "path": test_file_1
            },
            {
                "name": "file_open_executor.py",
                "path": test_file_2
            }
        ],
        2
    )

    print("Success :", result["success"])
    print("Selected:", result["selected"])

    if (
        result["success"]
        and result["selected"]["name"]
        == "file_open_executor.py"
    ):
        print("NUMBER SELECTION TEST: PASS")
        tests_passed += 1
    else:
        print("NUMBER SELECTION TEST: FAIL")

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    print("\n" + "-" * 45)
    print(f"Tests passed : {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("FILE SELECTION MANAGER TEST: PASS")
        print("STEP 9.13 TEST PASSED")
    else:
        print("FILE SELECTION MANAGER TEST: FAIL")

    print("-" * 45)
    
