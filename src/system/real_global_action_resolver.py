# ============================================================
# MYX - REAL GLOBAL ACTION RESOLVER
# STEP 11.9
# ============================================================

import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.real_global_search import RealGlobalSearch


class RealGlobalActionResolver:

    def __init__(self, search=None):

        self.search_engine = (
            search or RealGlobalSearch()
        )

        print(
            "[RealGlobalActionResolver] Initialized"
        )

    # ========================================================
    # NORMALIZE
    # ========================================================

    @staticmethod
    def normalize(command):

        return str(command or "").strip()

    # ========================================================
    # TARGET SCORE
    # ========================================================

    @staticmethod
    def target_score(record):

        score = 0

        item_type = str(
            getattr(record, "item_type", "")
        ).lower()

        name = str(
            getattr(record, "name", "")
        ).strip().lower()

        launchable = bool(
            getattr(record, "launchable", False)
        )

        capabilities = getattr(
            record,
            "capabilities",
            []
        )

        capabilities = [
            str(value).lower()
            for value in capabilities
        ]

        # ----------------------------------------------------
        # APPLICATION TARGET
        # ----------------------------------------------------

        if item_type == "application":
            score += 100

        # ----------------------------------------------------
        # FOLDER TARGET
        # ----------------------------------------------------

        if item_type == "folder":
            score += 80

        # Exact well-known folder names
        if item_type == "folder" and name in {
            "desktop",
            "documents",
            "downloads",
            "pictures",
            "music",
            "videos",
        }:
            score += 100

        # ----------------------------------------------------
        # LAUNCHABLE TARGET
        # ----------------------------------------------------

        if launchable:
            score += 100

        # ----------------------------------------------------
        # CAPABILITY-AWARE PREFERENCE
        # ----------------------------------------------------

        if "open" in capabilities:
            score += 20

        if "launch" in capabilities:
            score += 20

        # ----------------------------------------------------
        # FILES SHOULD NOT BEAT REAL FOLDERS/APPLICATIONS
        # ----------------------------------------------------

        if item_type == "file":
            score -= 100

        return score

    # ========================================================
    # RESOLVE
    # ========================================================

    def resolve(self, command):

        command = self.normalize(command)

        if not command:
            return {
                "success": False,
                "action": None,
                "query": "",
                "results": [],
                "count": 0,
                "selected": None,
                "needs_selection": False,
            }

        lowered = command.lower()

        action = "search"

        prefixes = [
            ("open ", "open"),
            ("launch ", "open"),
            ("start ", "open"),
            ("find ", "find"),
            ("search ", "search"),
            ("locate ", "locate"),
            ("show ", "show"),
            ("where is ", "locate"),
            ("where are ", "locate"),
        ]

        query = command

        for prefix, detected_action in prefixes:

            if lowered.startswith(prefix):

                action = detected_action

                query = command[
                    len(prefix):
                ].strip()

                break

        results = self.search_engine.search(query)

        # ====================================================
        # INTENT-AWARE TARGET RANKING
        # ====================================================

        ranked_results = list(results)

        if action == "open" and ranked_results:

            ranked_results.sort(
                key=self.target_score,
                reverse=True
            )

        # ====================================================
        # SELECTION DECISION
        # ====================================================

        selected = None
        needs_selection = False

        if action == "open":

            # One result = safe direct selection
            if len(ranked_results) == 1:

                selected = ranked_results[0]

            # Multiple results
            elif len(ranked_results) > 1:

                best_score = self.target_score(
                    ranked_results[0]
                )

                second_score = self.target_score(
                    ranked_results[1]
                )

                # Clear winner
                if best_score > second_score:

                    selected = ranked_results[0]

                # No clear winner
                else:

                    needs_selection = True

        # ====================================================
        # RESULT
        # ====================================================

        return {
            "success": True,
            "action": action,
            "query": query,
            "results": ranked_results,
            "count": len(ranked_results),
            "selected": selected,
            "needs_selection": needs_selection,
        }

    # ========================================================
    # TESTS
    # ========================================================

    def run_tests(self):

        passed = 0
        total = 5

        print()
        print("=" * 65)
        print("MYX REAL GLOBAL ACTION RESOLVER TEST")
        print("STEP 11.9")
        print("=" * 65)

        # ----------------------------------------------------
        # TEST 1 - EMPTY COMMAND
        # ----------------------------------------------------

        print("\n[TEST 1] Empty Command")

        result = self.resolve("")

        if (
            result["success"] is False
            and result["action"] is None
            and result["count"] == 0
        ):

            print("EMPTY COMMAND TEST: PASS")
            passed += 1

        else:

            print("EMPTY COMMAND TEST: FAIL")

        # ----------------------------------------------------
        # TEST 2 - ACTION DETECTION
        # ----------------------------------------------------

        print("\n[TEST 2] Action Detection")

        result = self.resolve("find python")

        if (
            result["success"] is True
            and result["action"] == "find"
            and result["query"] == "python"
        ):

            print("ACTION DETECTION TEST: PASS")
            passed += 1

        else:

            print("ACTION DETECTION TEST: FAIL")

        # ----------------------------------------------------
        # TEST 3 - RESULT STRUCTURE
        # ----------------------------------------------------

        print("\n[TEST 3] Result Structure")

        required = {
            "success",
            "action",
            "query",
            "results",
            "count",
            "selected",
            "needs_selection",
        }

        if required.issubset(result.keys()):

            print("RESULT STRUCTURE TEST: PASS")
            passed += 1

        else:

            print("RESULT STRUCTURE TEST: FAIL")

        # ----------------------------------------------------
        # TEST 4 - OPEN CHROME RESOLUTION
        # ----------------------------------------------------

        print("\n[TEST 4] Open Chrome")

        result = self.resolve("open chrome")

        if result["success"] is True:

            print(
                f"Found results : {result['count']}"
            )

            if result["selected"] is not None:

                selected = result["selected"]

                print(
                    "Selected      : "
                    f"{getattr(selected, 'name', selected)}"
                )

                print(
                    "Needs selection: "
                    f"{result['needs_selection']}"
                )

                print(
                    "OPEN TARGET RANKING TEST: PASS"
                )

                passed += 1

            else:

                print(
                    "OPEN TARGET RANKING TEST: "
                    "NO CLEAR TARGET"
                )

        else:

            print(
                "OPEN TARGET RANKING TEST: FAIL"
            )

        # ----------------------------------------------------
        # TEST 5 - PREFIXES
        # ----------------------------------------------------

        print("\n[TEST 5] Open/Launch/Start Prefixes")

        prefix_tests = [
            "open chrome",
            "launch chrome",
            "start chrome",
        ]

        prefix_passed = True

        for command in prefix_tests:

            result = self.resolve(command)

            if (
                result["success"] is not True
                or result["action"] != "open"
                or result["query"].lower() != "chrome"
            ):

                prefix_passed = False
                break

        if prefix_passed:

            print("PREFIX TEST: PASS")
            passed += 1

        else:

            print("PREFIX TEST: FAIL")

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        print()
        print("-" * 65)
        print(
            f"Tests passed : {passed}/{total}"
        )

        if passed == total:

            print(
                "REAL GLOBAL ACTION TEST: PASS"
            )

            print(
                "STEP 11.9 TEST PASSED"
            )

        else:

            print(
                "REAL GLOBAL ACTION TEST: FAIL"
            )

            print(
                "STEP 11.9 TEST FAILED"
            )

        print("-" * 65)

        return passed == total


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    resolver = RealGlobalActionResolver()

    resolver.run_tests()
    