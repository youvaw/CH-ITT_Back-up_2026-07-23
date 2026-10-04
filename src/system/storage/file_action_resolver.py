import os
import sys
import traceback

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.storage.file_search_intelligence import (
    FileSearchIntelligence,
)


class FileActionResolver:
    """
    MYX Step 9.10

    Resolves natural-language file actions.

    Current safe actions:
        find
        search
        locate
        show

    Destructive actions such as delete/move/overwrite
    are intentionally NOT executed here.
    """

    ACTION_ALIASES = {
        "find": "find",
        "search": "search",
        "locate": "locate",
        "show": "show",
        "open": "open",
    }

    def __init__(self):

        self.search_engine = FileSearchIntelligence()

        print("[FileActionResolver] Initialized")

    def normalize(self, text):

        return str(text).strip().lower()

    def detect_action(self, command):

        value = self.normalize(command)

        for alias, action in self.ACTION_ALIASES.items():

            if value.startswith(alias + " "):
                return action

            if value == alias:
                return action

        if value.startswith("where is "):
            return "locate"

        if value.startswith("where are "):
            return "locate"

        if value.startswith("look for "):
            return "search"

        return None

    def extract_query(self, command):

        value = self.normalize(command)

        prefixes = (
            "find ",
            "search for ",
            "search ",
            "locate ",
            "show ",
            "show me ",
            "open ",
            "where is ",
            "where are ",
            "look for ",
        )

        for prefix in prefixes:

            if value.startswith(prefix):

                return value[len(prefix):].strip()

        return value

    def resolve(self, command):

        action = self.detect_action(command)

        query = self.extract_query(command)

        if not query:

            return {
                "success": False,
                "action": action,
                "query": query,
                "results": [],
                "message": "No file query supplied.",
            }

        if action in (
            "find",
            "search",
            "locate",
            "show",
        ):

            results = self.search_engine.search(query)

            return {
                "success": True,
                "action": action,
                "query": query,
                "results": results,
                "count": len(results),
            }

        if action == "open":

            results = self.search_engine.search(query)

            return {
                "success": True,
                "action": "open",
                "query": query,
                "results": results,
                "count": len(results),
                "execution": "deferred",
            }

        return {
            "success": False,
            "action": None,
            "query": query,
            "results": [],
            "message": "Unknown file action.",
        }


def main():

    print("==========================================")
    print("    MYX STEP 9.10 FILE ACTION TEST")
    print("==========================================")

    try:

        resolver = FileActionResolver()

        passed = 0
        total = 4

        print("\n[TEST 1] Detect Find")

        action = resolver.detect_action(
            "find app"
        )

        print(
            f"Action: {action}"
        )

        if action == "find":
            print("ACTION DETECTION TEST: PASS")
            passed += 1
        else:
            print("ACTION DETECTION TEST: FAIL")

        print("\n[TEST 2] Query Extraction")

        query = resolver.extract_query(
            "find app"
        )

        print(
            f"Query: {query}"
        )

        if query == "app":
            print("QUERY EXTRACTION TEST: PASS")
            passed += 1
        else:
            print("QUERY EXTRACTION TEST: FAIL")

        print("\n[TEST 3] File Resolution")

        result = resolver.resolve(
            "find app"
        )

        print(
            f"Success : {result.get('success')}"
        )

        print(
            f"Results : {result.get('count', 0)}"
        )

        if result.get("success"):
            print("FILE RESOLUTION TEST: PASS")
            passed += 1
        else:
            print("FILE RESOLUTION TEST: FAIL")

        print("\n[TEST 4] Unknown Action")

        result = resolver.resolve(
            "something completely unknown"
        )

        print(
            f"Success : {result.get('success')}"
        )

        if result.get("success") is False:
            print("UNKNOWN ACTION TEST: PASS")
            passed += 1
        else:
            print("UNKNOWN ACTION TEST: FAIL")

        print("\n------------------------------------------")

        print(
            f"Tests passed : {passed}/{total}"
        )

        if passed == total:
            print("STEP 9.10 TEST: PASS")
        else:
            print("STEP 9.10 TEST: FAIL")

        print("------------------------------------------")

    except Exception:

        print("\n==========================================")
        print("STEP 9.10 ERROR")
        print("==========================================")

        traceback.print_exc()


if __name__ == "__main__":
    main()
    

