import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class FileResponseFormatter:
    """
    MYX STEP 9.15

    Converts file operation results into
    clean human-readable responses.

    This module only formats results.
    """

    def __init__(self):
        print("[FileResponseFormatter] Initialized")

    # =========================================================
    # HELPERS
    # =========================================================

    def normalize(self, value):
        if value is None:
            return ""

        return " ".join(
            str(value).strip().split()
        )

    def filename(self, path):
        if not path:
            return ""

        return os.path.basename(
            str(path).rstrip("\\/")
        )

    # =========================================================
    # SEARCH RESPONSE
    # =========================================================

    def format_search(self, result):

        if not result:
            return "No result information available."

        if not result.get("success", False):
            return result.get(
                "message",
                "I couldn't complete the file search."
            )

        action = result.get(
            "action",
            "search"
        )

        query = self.normalize(
            result.get("query", "")
        )

        results = result.get(
            "results",
            []
        )

        count = result.get(
            "count",
            len(results)
        )

        if count == 0:

            if query:
                return (
                    f"I couldn't find any files "
                    f"matching '{query}'."
                )

            return "I couldn't find any matching files."

        if count == 1:

            item = results[0]

            if isinstance(item, dict):

                path = (
                    item.get("path")
                    or item.get("full_path")
                    or item.get("file_path")
                )

            else:
                path = str(item)

            name = self.filename(path)

            if action == "locate":

                return (
                    f"I found {name}. "
                    f"It's located at {path}."
                )

            return f"I found {name}."

        return (
            f"I found {count} files matching "
            f"'{query}'."
        )

    # =========================================================
    # OPEN RESPONSE
    # =========================================================

    def format_open(self, result):

        if not result:
            return (
                "No open result information available."
            )

        # IMPORTANT:
        # Multiple candidates must be handled first.
        if result.get(
            "needs_selection",
            False
        ):
            return self.format_selection(result)

        if result.get(
            "success",
            False
        ):

            selected = result.get(
                "selected"
            )

            if isinstance(
                selected,
                dict
            ):

                path = (
                    selected.get("path")
                    or selected.get("full_path")
                    or selected.get("file_path")
                )

            else:
                path = selected

            name = self.filename(path)

            if name:
                return f"Opening {name}."

            return (
                "Opening the selected file."
            )

        return result.get(
            "message",
            "I couldn't open the requested file."
        )

    # =========================================================
    # SELECTION RESPONSE
    # =========================================================

    def format_selection(self, result):

        if not result:
            return (
                "No selection information available."
            )

        if result.get(
            "success",
            False
        ):

            selected = result.get(
                "selected"
            )

            if isinstance(
                selected,
                dict
            ):

                name = selected.get(
                    "name"
                )

                path = (
                    selected.get("path")
                    or selected.get("full_path")
                    or selected.get("file_path")
                )

                if name:
                    return f"Selected {name}."

                if path:
                    return (
                        f"Selected "
                        f"{self.filename(path)}."
                    )

            return "File selected."

        if result.get(
            "needs_selection",
            False
        ):

            options = (
                result.get("options")
                or result.get("candidates")
                or result.get("results")
                or result.get("files")
                or result.get("matches")
                or result.get("items")
                or []
            )

            if not options:
                return (
                    "No selectable files found."
                )

            lines = [
                "I found multiple matching files:"
            ]

            for index, option in enumerate(
                options,
                start=1
            ):

                if isinstance(
                    option,
                    dict
                ):

                    number = option.get(
                        "number",
                        index
                    )

                    name = (
                        option.get("name")
                        or self.filename(
                            option.get("path")
                            or option.get("full_path")
                            or option.get("file_path")
                            or ""
                        )
                    )

                else:

                    number = index

                    name = self.filename(
                        str(option)
                    )

                if not name:
                    name = "Unknown file"

                lines.append(
                    f"{number}. {name}"
                )

            return "\n".join(lines)

        return result.get(
            "message",
            "I couldn't determine "
            "the file selection."
        )

    # =========================================================
    # GENERIC FORMAT
    # =========================================================

    def format(self, result):

        if not result:
            return (
                "No file operation result available."
            )

        # IMPORTANT:
        # Selection always has highest priority.
        if result.get(
            "needs_selection",
            False
        ):
            return self.format_selection(
                result
            )

        action = result.get(
            "action"
        )

        if action == "open":
            return self.format_open(
                result
            )

        if action in (
            "find",
            "search",
            "locate",
            "show"
        ):
            return self.format_search(
                result
            )

        return result.get(
            "message",
            "File operation completed."
        )


# =============================================================
# STEP 9.15 TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 48)
    print("    MYX STEP 9.15 RESPONSE FORMATTER TEST")
    print("=" * 48)

    formatter = FileResponseFormatter()

    tests_passed = 0
    total_tests = 5

    test_file = os.path.join(
        PROJECT_ROOT,
        "src",
        "system",
        "file_action_resolver.py"
    )

    # ---------------------------------------------------------
    # TEST 1
    # ---------------------------------------------------------

    print("\n[TEST 1] Search Response")

    result = formatter.format({
        "success": True,
        "action": "search",
        "query": "app",
        "results": [
            {
                "name": "file_action_resolver.py",
                "path": test_file
            }
        ],
        "count": 1
    })

    print("Response:", result)

    if "found" in result.lower():

        print(
            "SEARCH RESPONSE TEST: PASS"
        )

        tests_passed += 1

    else:

        print(
            "SEARCH RESPONSE TEST: FAIL"
        )

    # ---------------------------------------------------------
    # TEST 2
    # ---------------------------------------------------------

    print("\n[TEST 2] Locate Response")

    result = formatter.format({
        "success": True,
        "action": "locate",
        "query": "app",
        "results": [
            {
                "name": "file_action_resolver.py",
                "path": test_file
            }
        ],
        "count": 1
    })

    print("Response:", result)

    if (
        "located" in result.lower()
        and "file_action_resolver.py"
        in result
    ):

        print(
            "LOCATE RESPONSE TEST: PASS"
        )

        tests_passed += 1

    else:

        print(
            "LOCATE RESPONSE TEST: FAIL"
        )

    # ---------------------------------------------------------
    # TEST 3
    # ---------------------------------------------------------

    print("\n[TEST 3] Multiple Results")

    result = formatter.format({
        "success": True,
        "action": "search",
        "query": "python",
        "results": [
            {
                "name": "python1.py",
                "path": test_file
            },
            {
                "name": "python2.py",
                "path": test_file
            },
            {
                "name": "python3.py",
                "path": test_file
            }
        ],
        "count": 3
    })

    print("Response:", result)

    if "3 files" in result:

        print(
            "MULTIPLE RESULT TEST: PASS"
        )

        tests_passed += 1

    else:

        print(
            "MULTIPLE RESULT TEST: FAIL"
        )

    # ---------------------------------------------------------
    # TEST 4
    # ---------------------------------------------------------

    print("\n[TEST 4] Open Success")

    result = formatter.format({
        "success": True,
        "action": "open",
        "selected": {
            "name": "file_action_resolver.py",
            "path": test_file
        },
        "count": 1
    })

    print("Response:", result)

    if "opening" in result.lower():

        print(
            "OPEN RESPONSE TEST: PASS"
        )

        tests_passed += 1

    else:

        print(
            "OPEN RESPONSE TEST: FAIL"
        )

    # ---------------------------------------------------------
    # TEST 5
    # ---------------------------------------------------------

    print("\n[TEST 5] Multiple Selection")

    second_file = os.path.join(
        PROJECT_ROOT,
        "src",
        "system",
        "file_open_executor.py"
    )

    result = formatter.format({
        "success": False,
        "action": "open",
        "needs_selection": True,
        "count": 2,
        "candidates": [
            {
                "name": "file_action_resolver.py",
                "path": test_file
            },
            {
                "name": "file_open_executor.py",
                "path": second_file
            }
        ]
    })

    print("Response:")
    print(result)

    if (
        "multiple" in result.lower()
        and "1." in result
        and "2." in result
        and "file_action_resolver.py"
        in result
        and "file_open_executor.py"
        in result
    ):

        print(
            "SELECTION RESPONSE TEST: PASS"
        )

        tests_passed += 1

    else:

        print(
            "SELECTION RESPONSE TEST: FAIL"
        )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    print("\n" + "-" * 48)

    print(
        f"Tests passed : "
        f"{tests_passed}/{total_tests}"
    )

    if tests_passed == total_tests:

        print(
            "FILE RESPONSE FORMATTER TEST: PASS"
        )

        print(
            "STEP 9.15 TEST PASSED"
        )

    else:

        print(
            "FILE RESPONSE FORMATTER TEST: FAIL"
        )

    print("-" * 48)

