import os
import sys


# ============================================================
# MYX PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# FILE RESPONSE FORMATTER
# ============================================================

class FileResponseFormatter:
    """
    MYX File Response Formatter

    Converts file operation results into human-readable
    responses.

    Responsibilities:
        - Search response
        - Locate response
        - Open response
        - Multiple-file selection response

    Does NOT:
        - Search files
        - Open files
        - Select files
        - Execute commands
    """

    def __init__(self):
        print("[FileResponseFormatter] Initialized")

    # --------------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------------

    def normalize(self, value):
        if value is None:
            return ""

        return str(value).strip()

    # --------------------------------------------------------
    # GET FILENAME
    # --------------------------------------------------------

    def filename(self, path):
        path = self.normalize(path)

        if not path:
            return ""

        return os.path.basename(path)

    # --------------------------------------------------------
    # EXTRACT PATH
    # --------------------------------------------------------

    def extract_path(self, item):
        """
        Extract path from a result item.

        Supports:
            string
            path
            file_path
            filepath
            full_path
            location
            target
        """

        if item is None:
            return ""

        # Direct string
        if isinstance(item, str):
            return self.normalize(item)

        # Dictionary
        if isinstance(item, dict):

            for key in (
                "path",
                "file_path",
                "filepath",
                "full_path",
                "location",
                "target",
            ):
                value = item.get(key)

                if value:
                    return self.normalize(value)

        return ""

    # --------------------------------------------------------
    # EXTRACT RESULT LIST
    # --------------------------------------------------------

    def extract_results(self, result):
        """
        Extract the list of matching files.

        Supported keys:
            candidates
            results
            files
            matches
            items
            options
        """

        if not isinstance(result, dict):
            return []

        for key in (
            "candidates",
            "results",
            "files",
            "matches",
            "items",
            "options",
        ):
            value = result.get(key)

            if isinstance(value, list):
                return value

        return []

    # --------------------------------------------------------
    # SEARCH RESPONSE
    # --------------------------------------------------------

    def format_search(self, result):

        if not result:
            return "No file operation result available."

        results = self.extract_results(result)

        if not results:
            return self.normalize(
                result.get(
                    "message",
                    "I couldn't find any matching files."
                )
            )

        # One result
        if len(results) == 1:

            path = self.extract_path(results[0])
            name = self.filename(path)

            if name:
                return f"I found {name}."

            return "I found one matching file."

        # Multiple results
        query = self.normalize(
            result.get("query", "")
        )

        if query:
            return (
                f"I found {len(results)} files "
                f"matching '{query}'."
            )

        return (
            f"I found {len(results)} matching files."
        )

    # --------------------------------------------------------
    # OPEN RESPONSE
    # --------------------------------------------------------

    def format_open(self, result):

        if not result:
            return "No file operation result available."

        if not result.get("success", False):
            return self.normalize(
                result.get(
                    "message",
                    "I couldn't open that file."
                )
            )

        selected = result.get("selected")

        if selected:
            path = self.extract_path(selected)
        else:
            path = self.extract_path(result)

        name = self.filename(path)

        if name:
            return f"Opening {name}."

        return "Opening the file."

    # --------------------------------------------------------
    # MULTIPLE SELECTION RESPONSE
    # --------------------------------------------------------

    def format_selection(self, result):

        results = self.extract_results(result)

        if not results:

            return (
                "I found multiple matching files, "
                "but I couldn't display the choices."
            )

        lines = []

        lines.append(
            f"I found {len(results)} matching files. "
            "Please choose which one you want to open:"
        )

        for index, item in enumerate(results, start=1):

            path = self.extract_path(item)

            if path:

                lines.append(
                    f"{index}. {path}"
                )

            else:

                lines.append(
                    f"{index}. Unknown file"
                )

        return "\n".join(lines)

    # --------------------------------------------------------
    # MAIN FORMAT FUNCTION
    # --------------------------------------------------------

 def format_open(self, result):

    if not result:
        return "No open result information available."

    # Multiple candidates always take priority.
    if result.get("needs_selection", False):
        return self.format_selection(result)

    if result.get("success", False):

        selected = result.get("selected")

        if isinstance(selected, dict):
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

        return "Opening the selected file."

    return result.get(
        "message",
        "I couldn't open the requested file."
    )
    # ========================================================
    # TEST 1
    # ========================================================

    print("\n[TEST 1] Search Response")

    result = {
        "success": True,
        "action": "find",
        "query": "file_action_resolver",
        "results": [
            {
                "path": test_file
            }
        ]
    }

    response = formatter.format(result)

    print("Response:", response)

    if response == "I found file_action_resolver.py.":

        print("SEARCH RESPONSE TEST: PASS")
        passed += 1

    else:

        print("SEARCH RESPONSE TEST: FAIL")

    # ========================================================
    # TEST 2
    # ========================================================

    print("\n[TEST 2] Locate Response")

    result = {
        "success": True,
        "action": "locate",
        "query": "file_action_resolver",
        "results": [
            {
                "path": test_file
            }
        ]
    }

    response = formatter.format(result)

    print(
        "Response:",
        response
    )

    if (
        "file_action_resolver.py" in response
        and test_file in response
    ):

        print("LOCATE RESPONSE TEST: PASS")
        passed += 1

    else:

        print("LOCATE RESPONSE TEST: FAIL")

    # ========================================================
    # TEST 3
    # ========================================================

    print("\n[TEST 3] Multiple Results")

    result = {
        "success": True,
        "action": "find",
        "query": "python",
        "results": [
            {
                "path": "Python Tutorial.pdf"
            },
            {
                "path": "Python Project.py"
            },
            {
                "path": "Python Notes.docx"
            },
        ]
    }

    response = formatter.format(result)

    print(
        "Response:",
        response
    )

    if (
        "I found 3 files" in response
        and "python" in response
    ):

        print("MULTIPLE RESULT TEST: PASS")
        passed += 1

    else:

        print("MULTIPLE RESULT TEST: FAIL")

    # ========================================================
    # TEST 4
    # ========================================================

    print("\n[TEST 4] Open Success")

    result = {
        "success": True,
        "action": "open",
        "selected": {
            "path": test_file
        }
    }

    response = formatter.format(result)

    print(
        "Response:",
        response
    )

    if response == "Opening file_action_resolver.py.":

        print("OPEN RESPONSE TEST: PASS")
        passed += 1

    else:

        print("OPEN RESPONSE TEST: FAIL")

    # ========================================================
    # TEST 5
    # ========================================================

    print("\n[TEST 5] Multiple Selection")

    result = {
        "success": True,
        "action": "open",
        "needs_selection": True,
        "results": [
            {
                "path": r"C:\Test\file_one.py"
            },
            {
                "path": r"C:\Test\file_two.py"
            }
        ]
    }

    response = formatter.format(result)

    print("Response:")
    print(response)

    expected_1 = (
        "I found 2 matching files. "
        "Please choose which one you want to open:"
    )

    expected_2 = (
        r"1. C:\Test\file_one.py"
    )

    expected_3 = (
        r"2. C:\Test\file_two.py"
    )

    if (
        expected_1 in response
        and expected_2 in response
        and expected_3 in response
    ):

        print("MULTIPLE SELECTION TEST: PASS")
        passed += 1

    else:

        print("MULTIPLE SELECTION TEST: FAIL")

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n" + "-" * 48)

    print(
        f"Tests passed : {passed}/{total}"
    )

    if passed == total:

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

        print(
            "STEP 9.15 TEST FAILED"
        )

    print("-" * 48)
    
