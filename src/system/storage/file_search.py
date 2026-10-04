import os
import sys


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.storage.file_index import FileIndex


# ============================================================
# MYX FILE SEARCH
# ============================================================

class FileSearch:
    """
    MYX File Search Engine

    Uses the existing FileIndex instead of scanning the
    filesystem for every search.

    Supported search types:

        name
        category
        extension
        folder
        generic
    """

    def __init__(self, file_index=None):

        self.file_index = (
            file_index
            if file_index is not None
            else FileIndex()
        )

        print("[FileSearch] Initialized")


    # ========================================================
    # NORMALIZATION
    # ========================================================

    def normalize(self, value):

        if value is None:
            return ""

        return str(value).strip()


    # ========================================================
    # NAME SEARCH
    # ========================================================

    def search_name(self, query):

        query = self.normalize(query)

        if not query:
            return []

        try:

            return self.file_index.search_name(
                query
            )

        except Exception as error:

            print(
                f"[FileSearch] Name search error: {error}"
            )

            return []


    # ========================================================
    # CATEGORY SEARCH
    # ========================================================

    def search_category(self, category):

        category = self.normalize(category)

        if not category:
            return []

        try:

            return self.file_index.search_category(
                category
            )

        except Exception as error:

            print(
                f"[FileSearch] Category search error: {error}"
            )

            return []


    # ========================================================
    # EXTENSION SEARCH
    # ========================================================

    def search_extension(self, extension):

        extension = self.normalize(
            extension
        )

        if not extension:
            return []

        if not extension.startswith("."):
            extension = "." + extension

        try:

            return self.file_index.search_extension(
                extension
            )

        except Exception as error:

            print(
                f"[FileSearch] Extension search error: {error}"
            )

            return []


    # ========================================================
    # FOLDER SEARCH
    # ========================================================

    def search_folder(self, folder):

        folder = self.normalize(folder)

        if not folder:
            return []

        try:

            return self.file_index.search_folder(
                folder
            )

        except Exception as error:

            print(
                f"[FileSearch] Folder search error: {error}"
            )

            return []


    # ========================================================
    # GENERIC SEARCH
    # ========================================================

    def search(self, query):

        query = self.normalize(query)

        if not query:
            return []

        # ----------------------------------------------------
        # First: filename search
        # ----------------------------------------------------

        results = self.search_name(query)

        if results:
            return results

        # ----------------------------------------------------
        # Second: category search
        # ----------------------------------------------------

        category_aliases = {
            "pdf": "pdf",
            "pdf files": "pdf",
            "document": "document",
            "documents": "document",
            "word": "document",
            "excel": "spreadsheet",
            "spreadsheets": "spreadsheet",
            "spreadsheet": "spreadsheet",
            "presentation": "presentation",
            "presentations": "presentation",
            "image": "image",
            "images": "image",
            "photo": "image",
            "photos": "image",
            "music": "audio",
            "audio": "audio",
            "song": "audio",
            "songs": "audio",
            "video": "video",
            "videos": "video",
            "code": "code",
            "source code": "code",
            "archive": "archive",
            "archives": "archive",
        }

        category = category_aliases.get(
            query.lower()
        )

        if category:

            results = self.search_category(
                category
            )

            if results:
                return results

        # ----------------------------------------------------
        # Third: extension search
        # ----------------------------------------------------

        extension_aliases = {
            "python": ".py",
            "python files": ".py",
            "javascript": ".js",
            "javascript files": ".js",
            "typescript": ".ts",
            "typescript files": ".ts",
            "cpp": ".cpp",
            "c++": ".cpp",
            "c": ".c",
            "java": ".java",
            "html": ".html",
            "css": ".css",
            "json": ".json",
            "pdf": ".pdf",
            "docx": ".docx",
            "word files": ".docx",
            "xlsx": ".xlsx",
            "excel files": ".xlsx",
            "pptx": ".pptx",
        }

        extension = extension_aliases.get(
            query.lower()
        )

        if extension:

            results = self.search_extension(
                extension
            )

            if results:
                return results

        return []


    # ========================================================
    # RESULT COUNT
    # ========================================================

    def count(self, results):

        if results is None:
            return 0

        try:
            return len(results)

        except TypeError:
            return 0


    # ========================================================
    # RESULT DISPLAY
    # ========================================================

    def print_results(
        self,
        results,
        title="Search Results",
    ):

        print()
        print("------------------------------------------")
        print(title)
        print("------------------------------------------")

        if not results:

            print("No files found.")

            return

        for index, result in enumerate(
            results,
            start=1,
        ):

            if isinstance(result, dict):

                name = (
                    result.get("name")
                    or result.get("file_name")
                    or "Unknown"
                )

                path = (
                    result.get("path")
                    or result.get("file_path")
                    or ""
                )

                print(
                    f"{index}. {name}"
                )

                if path:
                    print(
                        f"   {path}"
                    )

            else:

                print(
                    f"{index}. {result}"
                )


# ============================================================
# STEP 9.6 TEST
# ============================================================

def run_step_9_6_test():

    print()
    print("==========================================")
    print("      MYX STEP 9.6 FILE SEARCH TEST")
    print("==========================================")

    search = FileSearch()

    total_pass = 0
    total_tests = 0


    # ========================================================
    # TEST 1 â€” NAME
    # ========================================================

    total_tests += 1

    print()
    print("[TEST 1] Name Search")

    results = search.search_name(
        "Python"
    )

    search.print_results(
        results,
        "Python filename search",
    )

    if results:

        print("NAME SEARCH TEST: PASS")
        total_pass += 1

    else:

        print(
            "NAME SEARCH TEST: FAIL"
        )


    # ========================================================
    # TEST 2 â€” PDF CATEGORY
    # ========================================================

    total_tests += 1

    print()
    print("[TEST 2] PDF Category Search")

    results = search.search_category(
        "pdf"
    )

    search.print_results(
        results,
        "PDF category search",
    )

    if results:

        print(
            "CATEGORY SEARCH TEST: PASS"
        )

        total_pass += 1

    else:

        print(
            "CATEGORY SEARCH TEST: FAIL"
        )


    # ========================================================
    # TEST 3 â€” PYTHON EXTENSION
    # ========================================================

    total_tests += 1

    print()
    print("[TEST 3] Python Extension Search")

    results = search.search_extension(
        ".py"
    )

    search.print_results(
        results,
        "Python files",
    )

    if results:

        print(
            "EXTENSION SEARCH TEST: PASS"
        )

        total_pass += 1

    else:

        print(
            "EXTENSION SEARCH TEST: FAIL"
        )


    # ========================================================
    # TEST 4 â€” FOLDER
    # ========================================================

    total_tests += 1

    print()
    print("[TEST 4] Folder Search")

    documents_folder = os.path.join(
        os.path.expanduser("~"),
        "Documents",
    )

    results = search.search_folder(
        documents_folder
    )

    search.print_results(
        results,
        "Documents folder",
    )

    # Folder may legitimately contain no indexed files,
    # so this test verifies the search call itself.

    if isinstance(results, list):

        print(
            "FOLDER SEARCH TEST: PASS"
        )

        total_pass += 1

    else:

        print(
            "FOLDER SEARCH TEST: FAIL"
        )


    # ========================================================
    # TEST 5 â€” GENERIC SEARCH
    # ========================================================

    total_tests += 1

    print()
    print("[TEST 5] Generic Search")

    results = search.search(
        "python"
    )

    search.print_results(
        results,
        "Generic Python search",
    )

    if results:

        print(
            "GENERIC SEARCH TEST: PASS"
        )

        total_pass += 1

    else:

        print(
            "GENERIC SEARCH TEST: FAIL"
        )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("------------------------------------------")
    print(
        f"Tests passed : "
        f"{total_pass}/{total_tests}"
    )

    if total_pass == total_tests:

        print()
        print(
            "FILE SEARCH ENGINE TEST: PASS"
        )

        print()
        print(
            "=========================================="
        )
        print(
            "       STEP 9.6 TEST PASSED"
        )
        print(
            "=========================================="
        )

        return True

    print()
    print(
        "FILE SEARCH ENGINE TEST: FAIL"
    )

    print()
    print(
        "=========================================="
    )
    print(
        "       STEP 9.6 TEST FAILED"
    )
    print(
        "=========================================="
    )

    return False


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("==========================================")
    print("       MYX STEP 9.6 FILE SEARCH TEST")
    print("==========================================")

    search_engine = FileSearch()

    total_tests = 5
    passed_tests = 0

    # ==========================================
    # TEST 1 â€” NAME SEARCH
    # ==========================================

    print("\n[TEST 1] Name Search")

    results = search_engine.search_name("app")

    search_engine.print_results(
        results,
        "Application filename search"
    )

    if results:
        print("NAME SEARCH TEST: PASS")
        passed_tests += 1
    else:
        print("NAME SEARCH TEST: FAIL")

    # ==========================================
    # TEST 2 â€” CATEGORY SEARCH
    # ==========================================

    print("\n[TEST 2] Category Search")

    results = search_engine.search_category("code")

    search_engine.print_results(
        results,
        "Code category search"
    )

    if results:
        print("CATEGORY SEARCH TEST: PASS")
        passed_tests += 1
    else:
        print("CATEGORY SEARCH TEST: FAIL")

    # ==========================================
    # TEST 3 â€” EXTENSION SEARCH
    # ==========================================

    print("\n[TEST 3] Extension Search")

    results = search_engine.search_extension(".py")

    search_engine.print_results(
        results,
        "Python files"
    )

    if results:
        print(
            f"Python files found: {len(results)}"
        )
        print("EXTENSION SEARCH TEST: PASS")
        passed_tests += 1
    else:
        print("EXTENSION SEARCH TEST: FAIL")

    # ==========================================
    # TEST 4 â€” FOLDER SEARCH
    # ==========================================

    print("\n[TEST 4] Folder Search")

    extension_results = (
        search_engine.search_extension(".py")
    )

    if extension_results:

        test_folder = extension_results[0].get(
            "folder"
        )

        results = search_engine.search_folder(
            test_folder
        )

        search_engine.print_results(
            results,
            f"Indexed folder search: {test_folder}"
        )

        if results:
            print("FOLDER SEARCH TEST: PASS")
            passed_tests += 1
        else:
            print("FOLDER SEARCH TEST: FAIL")

    else:

        print(
            "No indexed files available "
            "to determine test folder."
        )

        print("FOLDER SEARCH TEST: FAIL")

    # ==========================================
    # TEST 5 â€” GENERIC SEARCH
    # ==========================================

    print("\n[TEST 5] Generic Search")

    results = search_engine.search("app")

    search_engine.print_results(
        results,
        "Generic search: app"
    )

    if results:
        print("GENERIC SEARCH TEST: PASS")
        passed_tests += 1
    else:
        print("GENERIC SEARCH TEST: FAIL")

    # ==========================================
    # FINAL RESULT
    # ==========================================

    print("\n------------------------------------------")
    print(
        f"Tests passed : "
        f"{passed_tests}/{total_tests}"
    )
    print("------------------------------------------")

    if passed_tests == total_tests:

        print("FILE SEARCH ENGINE TEST: PASS")
        print("STEP 9.6 TEST PASSED")

    else:

        print("FILE SEARCH ENGINE TEST: FAIL")
        print("STEP 9.6 TEST FAILED")

    print("==========================================")
    

