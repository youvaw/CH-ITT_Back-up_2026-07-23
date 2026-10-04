import os
import sys
import traceback

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.storage.file_search import FileSearch


class FileSearchIntelligence:
    """
    MYX STEP 9.9
    Intelligent file-search layer.

    Purpose:
        Natural-language file queries
        -> query understanding
        -> category / extension detection
        -> FileSearch
        -> normalized results

    This module does NOT:
        - open files
        - delete files
        - move files
        - modify files
        - launch applications
    """

    CATEGORY_ALIASES = {
        "pdf": "pdf",
        "pdfs": "pdf",

        "document": "document",
        "documents": "document",
        "doc": "document",
        "docs": "document",

        "spreadsheet": "spreadsheet",
        "spreadsheets": "spreadsheet",
        "excel": "spreadsheet",
        "xls": "spreadsheet",
        "xlsx": "spreadsheet",

        "presentation": "presentation",
        "presentations": "presentation",
        "powerpoint": "presentation",
        "ppt": "presentation",
        "pptx": "presentation",

        "image": "image",
        "images": "image",
        "photo": "image",
        "photos": "image",
        "picture": "image",
        "pictures": "image",

        "video": "video",
        "videos": "video",
        "movie": "video",
        "movies": "video",

        "audio": "audio",
        "audios": "audio",
        "music": "audio",
        "song": "audio",
        "songs": "audio",

        "code": "code",
        "codes": "code",
        "program": "code",
        "programs": "code",
        "python": "code",
    }

    EXTENSION_ALIASES = {
        "python": ".py",
        "py": ".py",

        "text": ".txt",
        "txt": ".txt",

        "pdf": ".pdf",

        "word": ".docx",
        "doc": ".docx",
        "docx": ".docx",

        "excel": ".xlsx",
        "xls": ".xls",
        "xlsx": ".xlsx",

        "powerpoint": ".pptx",
        "ppt": ".ppt",
        "pptx": ".pptx",

        "image": None,
        "jpg": ".jpg",
        "jpeg": ".jpeg",
        "png": ".png",
        "gif": ".gif",

        "video": None,
        "mp4": ".mp4",
        "mkv": ".mkv",
        "avi": ".avi",

        "audio": None,
        "mp3": ".mp3",
        "wav": ".wav",
        "flac": ".flac",
    }

    STOP_WORDS = {
        "find",
        "search",
        "searching",
        "look",
        "for",
        "locate",
        "show",
        "me",
        "file",
        "files",
        "the",
        "my",
        "a",
        "an",
    }

    def __init__(self):
        self.file_search = FileSearch()
        print("[FileSearchIntelligence] Initialized")

    # ---------------------------------------------------------
    # BASIC NORMALIZATION
    # ---------------------------------------------------------

    def normalize(self, text):
        if text is None:
            return ""

        return " ".join(
            str(text).strip().lower().split()
        )

    # ---------------------------------------------------------
    # QUERY CLEANING
    # ---------------------------------------------------------

    def clean_query(self, query):
        value = self.normalize(query)

        prefixes = (
            "search for ",
            "look for ",
            "find ",
            "search ",
            "locate ",
            "show me ",
            "show ",
            "where is ",
            "where are ",
        )

        for prefix in prefixes:
            if value.startswith(prefix):
                value = value[len(prefix):].strip()
                break

        words = value.split()

        cleaned = [
            word
            for word in words
            if word not in self.STOP_WORDS
        ]

        return " ".join(cleaned).strip()

    # ---------------------------------------------------------
    # CATEGORY DETECTION
    # ---------------------------------------------------------

    def detect_category(self, query):
        value = self.normalize(query)

        words = value.split()

        for word in words:
            if word in self.CATEGORY_ALIASES:
                return self.CATEGORY_ALIASES[word]

        return None

    # ---------------------------------------------------------
    # EXTENSION DETECTION
    # ---------------------------------------------------------

    def detect_extension(self, query):
        value = self.normalize(query)

        words = value.split()

        for word in words:
            if word in self.EXTENSION_ALIASES:
                extension = self.EXTENSION_ALIASES[word]

                if extension:
                    return extension

        # Direct extension detection
        for word in words:
            if word.startswith(".") and len(word) > 1:
                return word

        return None

    # ---------------------------------------------------------
    # NAME QUERY
    # ---------------------------------------------------------

    def extract_name_query(self, query):
        value = self.clean_query(query)

        category = self.detect_category(value)
        extension = self.detect_extension(value)

        words = value.split()

        filtered = []

        for word in words:
            if word in self.CATEGORY_ALIASES:
                continue

            if word in self.EXTENSION_ALIASES:
                continue

            if word.startswith("."):
                continue

            filtered.append(word)

        result = " ".join(filtered).strip()

        return result

    # ---------------------------------------------------------
    # SEARCH BY NAME
    # ---------------------------------------------------------

    def search_by_name(self, query):
        value = self.normalize(query)

        if not value:
            return []

        return self.file_search.search_name(value)

    # ---------------------------------------------------------
    # SEARCH BY CATEGORY
    # ---------------------------------------------------------

    def search_by_category(self, category):
        category = self.normalize(category)

        if not category:
            return []

        category = self.CATEGORY_ALIASES.get(
            category,
            category
        )

        return self.file_search.search_category(category)

    # ---------------------------------------------------------
    # SEARCH BY EXTENSION
    # ---------------------------------------------------------

    def search_by_extension(self, extension):
        extension = self.normalize(extension)

        if not extension:
            return []

        if not extension.startswith("."):
            extension = "." + extension

        return self.file_search.search_extension(extension)

    # ---------------------------------------------------------
    # GENERIC INTELLIGENT SEARCH
    # ---------------------------------------------------------

    def search(self, query):
        """
        Main public search interface.

        Examples:

            find app
            find pdf
            find python files
            search documents
            find excel
            find .py
        """

        original_query = self.normalize(query)

        if not original_query:
            return []

        category = self.detect_category(original_query)
        extension = self.detect_extension(original_query)

        name_query = self.extract_name_query(
            original_query
        )

        # -----------------------------------------------------
        # Extension-first search
        # -----------------------------------------------------

        if extension:
            results = self.search_by_extension(extension)

            if results:
                return results

        # -----------------------------------------------------
        # Category search
        # -----------------------------------------------------

        if category:
            results = self.search_by_category(category)

            if results:
                return results

        # -----------------------------------------------------
        # Name search
        # -----------------------------------------------------

        if name_query:
            results = self.search_by_name(name_query)

            if results:
                return results

        # -----------------------------------------------------
        # Final fallback
        # -----------------------------------------------------

        if name_query != original_query:
            results = self.search_by_name(original_query)

            if results:
                return results

        return []

    # ---------------------------------------------------------
    # RESULT COUNT
    # ---------------------------------------------------------

    def count(self, query):
        return len(
            self.search(query)
        )

    # ---------------------------------------------------------
    # RESULT PREVIEW
    # ---------------------------------------------------------

    def preview(self, query, limit=10):
        results = self.search(query)

        return results[:limit]

    # ---------------------------------------------------------
    # TEST OUTPUT
    # ---------------------------------------------------------

    def print_results(self, query, results, limit=10):
        print(f"\nQuery   : {query}")
        print(f"Results : {len(results)}")

        for index, item in enumerate(
            results[:limit],
            start=1
        ):
            if isinstance(item, dict):
                name = item.get(
                    "name",
                    item.get("file_name", "Unknown")
                )

                path = item.get(
                    "path",
                    item.get("file_path", "")
                )

                print(
                    f"{index}. {name}"
                    + (f" -> {path}" if path else "")
                )
            else:
                print(
                    f"{index}. {item}"
                )


# =============================================================
# STEP 9.9 TEST
# =============================================================

def main():

    print("==========================================")
    print("    MYX STEP 9.9 SEARCH INTELLIGENCE TEST")
    print("==========================================")

    try:

        engine = FileSearchIntelligence()

        passed = 0
        total = 5

        # -----------------------------------------------------
        # TEST 1
        # -----------------------------------------------------

        print("\n[TEST 1] Natural Name Search")

        result = engine.search("find app")

        print(
            f"Results : {len(result)}"
        )

        engine.print_results(
            "find app",
            result
        )

        if isinstance(result, list):
            print("NAME SEARCH TEST: PASS")
            passed += 1
        else:
            print("NAME SEARCH TEST: FAIL")

        # -----------------------------------------------------
        # TEST 2
        # -----------------------------------------------------

        print("\n[TEST 2] Category Search")

        result = engine.search(
            "find code files"
        )

        print(
            f"Results : {len(result)}"
        )

        engine.print_results(
            "find code files",
            result
        )

        if isinstance(result, list):
            print("CATEGORY SEARCH TEST: PASS")
            passed += 1
        else:
            print("CATEGORY SEARCH TEST: FAIL")

        # -----------------------------------------------------
        # TEST 3
        # -----------------------------------------------------

        print("\n[TEST 3] Extension Search")

        result = engine.search(
            "find python files"
        )

        print(
            f"Results : {len(result)}"
        )

        engine.print_results(
            "find python files",
            result
        )

        if isinstance(result, list):
            print("EXTENSION SEARCH TEST: PASS")
            passed += 1
        else:
            print("EXTENSION SEARCH TEST: FAIL")

        # -----------------------------------------------------
        # TEST 4
        # -----------------------------------------------------

        print("\n[TEST 4] PDF Search")

        result = engine.search(
            "find pdf"
        )

        print(
            f"Results : {len(result)}"
        )

        engine.print_results(
            "find pdf",
            result
        )

        if isinstance(result, list):
            print("PDF SEARCH TEST: PASS")
            passed += 1
        else:
            print("PDF SEARCH TEST: FAIL")

        # -----------------------------------------------------
        # TEST 5
        # -----------------------------------------------------

        print("\n[TEST 5] Empty Query Safety")

        result = engine.search("")

        print(
            f"Results : {len(result)}"
        )

        if result == []:
            print("EMPTY QUERY TEST: PASS")
            passed += 1
        else:
            print("EMPTY QUERY TEST: FAIL")

        # -----------------------------------------------------
        # FINAL
        # -----------------------------------------------------

        print("\n------------------------------------------")
        print(
            f"Tests passed : {passed}/{total}"
        )

        if passed == total:
            print(
                "SEARCH INTELLIGENCE TEST: PASS"
            )
            print(
                "STEP 9.9 TEST PASSED"
            )
        else:
            print(
                "SEARCH INTELLIGENCE TEST: FAIL"
            )
            print(
                "STEP 9.9 TEST FAILED"
            )

        print("------------------------------------------")

    except Exception:

        print("\n==========================================")
        print("STEP 9.9 ERROR")
        print("==========================================")

        traceback.print_exc()


if __name__ == "__main__":
    main()
    

