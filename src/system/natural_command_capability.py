import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class NaturalCommandCapability:
    """
    Converts natural MYX commands into generic capabilities.

    Examples:
        Open Chrome
            -> capability=open
            -> query=Chrome

        Find Python files
            -> capability=find
            -> query=Python files

        Show me Python files
            -> capability=show
            -> query=Python files
    """

    PATTERNS = [
        # IMPORTANT:
        # Longer patterns must come before shorter patterns.
        ("show me ", "show"),
        ("where can i find ", "locate"),
        ("search for ", "find"),
        ("where are ", "find"),
        ("where is ", "find"),
        ("show ", "show"),
        ("display ", "show"),
        ("find ", "find"),
        ("locate ", "locate"),
        ("select ", "select"),
        ("choose ", "select"),
        ("pick ", "select"),
        ("open ", "open"),
        ("launch ", "open"),
        ("start ", "open"),
        ("run ", "open"),
    ]

    def __init__(self):
        print("[NaturalCommandCapability] Initialized")

    def resolve(self, command):
        command = self._normalize(command)

        if not command:
            return {
                "success": False,
                "capability": None,
                "query": "",
                "command": "",
            }

        for pattern, capability in self.PATTERNS:
            if command.startswith(pattern):
                query = command[len(pattern):].strip()

                if not query:
                    return {
                        "success": False,
                        "capability": capability,
                        "query": "",
                        "command": command,
                    }

                return {
                    "success": True,
                    "capability": capability,
                    "query": query,
                    "command": command,
                }

        return {
            "success": False,
            "capability": None,
            "query": command,
            "command": command,
        }

    def capability(self, command):
        result = self.resolve(command)
        return result.get("capability")

    def query(self, command):
        result = self.resolve(command)
        return result.get("query", "")

    @staticmethod
    def _normalize(value):
        if value is None:
            return ""

        return " ".join(
            str(value).strip().lower().split()
        )


if __name__ == "__main__":
    print("=" * 60)
    print("    MYX STEP 10.6 NATURAL COMMAND CAPABILITY TEST")
    print("=" * 60)

    parser = NaturalCommandCapability()

    print("\n[TEST 1] Open Command")

    result = parser.resolve("Open Chrome")

    test1 = (
        result["success"]
        and result["capability"] == "open"
        and result["query"] == "chrome"
    )

    print("Result:", result)

    print(
        "OPEN COMMAND TEST:",
        "PASS" if test1 else "FAIL"
    )

    print("\n[TEST 2] Find Command")

    result = parser.resolve(
        "Find Python Tutorial.pdf"
    )

    test2 = (
        result["success"]
        and result["capability"] == "find"
        and result["query"] == "python tutorial.pdf"
    )

    print("Result:", result)

    print(
        "FIND COMMAND TEST:",
        "PASS" if test2 else "FAIL"
    )

    print("\n[TEST 3] Where Is Command")

    result = parser.resolve(
        "Where is my project"
    )

    test3 = (
        result["success"]
        and result["capability"] == "find"
        and result["query"] == "my project"
    )

    print("Result:", result)

    print(
        "WHERE IS TEST:",
        "PASS" if test3 else "FAIL"
    )

    print("\n[TEST 4] Show Me Command")

    result = parser.resolve(
        "Show me Python files"
    )

    test4 = (
        result["success"]
        and result["capability"] == "show"
        and result["query"] == "python files"
    )

    print("Result:", result)

    print(
        "SHOW ME TEST:",
        "PASS" if test4 else "FAIL"
    )

    print("\n[TEST 5] Unknown Command Safety")

    result = parser.resolve(
        "Hello MYX"
    )

    test5 = (
        result["success"] is False
        and result["capability"] is None
    )

    print("Result:", result)

    print(
        "UNKNOWN COMMAND TEST:",
        "PASS" if test5 else "FAIL"
    )

    tests = [
        test1,
        test2,
        test3,
        test4,
        test5,
    ]

    passed = sum(tests)

    print("\n" + "-" * 60)
    print(f"Tests passed : {passed}/5")

    if passed == 5:
        print("NATURAL COMMAND CAPABILITY TEST: PASS")
        print("STEP 10.6 TEST PASSED")
    else:
        print("NATURAL COMMAND CAPABILITY TEST: FAIL")
        print("STEP 10.6 TEST FAILED")

    print("-" * 60)
    
