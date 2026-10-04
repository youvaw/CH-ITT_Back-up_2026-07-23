import os
import sys


# ============================================================
# PROJECT BOOTSTRAP
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEM_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.dirname(SYSTEM_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# GLOBAL ACTION SAFETY MANAGER
# ============================================================

class GlobalActionSafetyManager:
    """
    MYX Global Action Safety Manager

    Purpose:
        Decide whether a resolved global action should:

        - execute
        - select
        - confirm
        - reject

    IMPORTANT:
        This module DOES NOT execute anything.

        It is only a safety decision layer between
        command planning and real execution.
    """

    SAFE_ACTIONS = {
        "find",
        "search",
        "locate",
        "show",
    }

    CONFIRM_ACTIONS = {
        "open",
        "launch",
        "start",
        "run",
    }

    REJECT_ACTIONS = {
        "",
        "unknown",
        "invalid",
        "delete",
        "remove",
        "format",
        "shutdown",
        "restart",
    }

    def __init__(self):
        print("[GlobalActionSafetyManager] Initialized")

    # ========================================================
    # NORMALIZATION
    # ========================================================

    def normalize(self, value):
        if value is None:
            return ""

        return str(value).strip().lower()

    # ========================================================
    # ACTION CLASSIFICATION
    # ========================================================

    def classify_action(self, action):
        action = self.normalize(action)

        if action in self.SAFE_ACTIONS:
            return "safe"

        if action in self.CONFIRM_ACTIONS:
            return "confirm"

        if action in self.REJECT_ACTIONS:
            return "reject"

        return "unknown"

    # ========================================================
    # PLAN HELPERS
    # ========================================================

    def get_action(self, plan):
        if not isinstance(plan, dict):
            return ""

        return self.normalize(plan.get("action"))

    def get_results(self, plan):
        if not isinstance(plan, dict):
            return []

        results = plan.get("results", [])

        if results is None:
            return []

        if not isinstance(results, list):
            return [results]

        return results

    def candidate_count(self, plan):
        return len(self.get_results(plan))

    def has_results(self, plan):
        return self.candidate_count(plan) > 0

    # ========================================================
    # SAFETY EVALUATION
    # ========================================================

    def evaluate(self, plan):
        """
        Return a safety decision.

        Possible decisions:

            execute
            select
            confirm
            reject
        """

        if not isinstance(plan, dict):
            return {
                "decision": "reject",
                "reason": "Invalid action plan.",
                "action": "",
                "candidate_count": 0,
            }

        action = self.get_action(plan)
        results = self.get_results(plan)
        count = len(results)

        # ----------------------------------------------------
        # Empty action
        # ----------------------------------------------------

        if not action:
            return {
                "decision": "reject",
                "reason": "No action specified.",
                "action": action,
                "candidate_count": count,
            }

        # ----------------------------------------------------
        # Explicitly rejected actions
        # ----------------------------------------------------

        if action in self.REJECT_ACTIONS:
            return {
                "decision": "reject",
                "reason": f"Action '{action}' is not allowed.",
                "action": action,
                "candidate_count": count,
            }

        # ----------------------------------------------------
        # Unknown action
        # ----------------------------------------------------

        action_type = self.classify_action(action)

        if action_type == "unknown":
            return {
                "decision": "reject",
                "reason": f"Unknown action '{action}'.",
                "action": action,
                "candidate_count": count,
            }

        # ----------------------------------------------------
        # No results
        # ----------------------------------------------------

        if count == 0:
            return {
                "decision": "reject",
                "reason": "No matching result found.",
                "action": action,
                "candidate_count": 0,
            }

        # ----------------------------------------------------
        # SAFE ACTION
        # ----------------------------------------------------

        if action_type == "safe":

            if count == 1:
                return {
                    "decision": "execute",
                    "reason": "Safe action with one result.",
                    "action": action,
                    "candidate_count": count,
                }

            return {
                "decision": "select",
                "reason": "Multiple results require selection.",
                "action": action,
                "candidate_count": count,
            }

        # ----------------------------------------------------
        # CONFIRM ACTION
        # ----------------------------------------------------

        if action_type == "confirm":

            if count == 1:
                return {
                    "decision": "confirm",
                    "reason": "Action requires user confirmation.",
                    "action": action,
                    "candidate_count": count,
                }

            return {
                "decision": "select",
                "reason": "Multiple candidates require selection.",
                "action": action,
                "candidate_count": count,
            }

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        return {
            "decision": "reject",
            "reason": "Safety evaluation failed.",
            "action": action,
            "candidate_count": count,
        }

    # ========================================================
    # DECISION HELPERS
    # ========================================================

    def is_safe(self, plan):
        decision = self.evaluate(plan)
        return decision["decision"] in {
            "execute",
            "select",
        }

    def requires_selection(self, plan):
        decision = self.evaluate(plan)
        return decision["decision"] == "select"

    def requires_confirmation(self, plan):
        decision = self.evaluate(plan)
        return decision["decision"] == "confirm"

    def is_rejected(self, plan):
        decision = self.evaluate(plan)
        return decision["decision"] == "reject"

    # ========================================================
    # DEBUG
    # ========================================================

    def print_decision(self, plan):
        decision = self.evaluate(plan)

        print("\n------------------------------------------")
        print("MYX ACTION SAFETY DECISION")
        print("------------------------------------------")
        print("Action           :", decision["action"])
        print("Candidate Count  :", decision["candidate_count"])
        print("Decision         :", decision["decision"])
        print("Reason           :", decision["reason"])
        print("------------------------------------------")

        return decision


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("==========================================")
    print("MYX STEP 11.14 GLOBAL ACTION SAFETY TEST")
    print("==========================================")

    manager = GlobalActionSafetyManager()

    tests_passed = 0
    total_tests = 7

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    print("\n[TEST 1] Manager Initialization")

    if isinstance(manager, GlobalActionSafetyManager):
        print("INITIALIZATION TEST: PASS")
        tests_passed += 1
    else:
        print("INITIALIZATION TEST: FAIL")

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    print("\n[TEST 2] Safe Single Result")

    plan = {
        "action": "find",
        "results": [
            {"name": "Google Chrome"}
        ],
    }

    result = manager.evaluate(plan)

    if result["decision"] == "execute":
        print("SAFE SINGLE RESULT TEST: PASS")
        tests_passed += 1
    else:
        print("SAFE SINGLE RESULT TEST: FAIL")

    # --------------------------------------------------------
    # TEST 3
    # --------------------------------------------------------

    print("\n[TEST 3] Multiple Results")

    plan = {
        "action": "find",
        "results": [
            {"name": "Chrome"},
            {"name": "Chrome Setup"},
        ],
    }

    result = manager.evaluate(plan)

    if result["decision"] == "select":
        print("MULTIPLE RESULT TEST: PASS")
        tests_passed += 1
    else:
        print("MULTIPLE RESULT TEST: FAIL")

    # --------------------------------------------------------
    # TEST 4
    # --------------------------------------------------------

    print("\n[TEST 4] Open Requires Confirmation")

    plan = {
        "action": "open",
        "results": [
            {"name": "Google Chrome"}
        ],
    }

    result = manager.evaluate(plan)

    if result["decision"] == "confirm":
        print("CONFIRMATION TEST: PASS")
        tests_passed += 1
    else:
        print("CONFIRMATION TEST: FAIL")

    # --------------------------------------------------------
    # TEST 5
    # --------------------------------------------------------

    print("\n[TEST 5] Empty Results")

    plan = {
        "action": "find",
        "results": [],
    }

    result = manager.evaluate(plan)

    if result["decision"] == "reject":
        print("EMPTY RESULT TEST: PASS")
        tests_passed += 1
    else:
        print("EMPTY RESULT TEST: FAIL")

    # --------------------------------------------------------
    # TEST 6
    # --------------------------------------------------------

    print("\n[TEST 6] Unknown Action")

    plan = {
        "action": "something_unknown",
        "results": [
            {"name": "Test"}
        ],
    }

    result = manager.evaluate(plan)

    if result["decision"] == "reject":
        print("UNKNOWN ACTION TEST: PASS")
        tests_passed += 1
    else:
        print("UNKNOWN ACTION TEST: FAIL")

    # --------------------------------------------------------
    # TEST 7
    # --------------------------------------------------------

    print("\n[TEST 7] Dangerous Action")

    plan = {
        "action": "delete",
        "results": [
            {"name": "Test File"}
        ],
    }

    result = manager.evaluate(plan)

    if result["decision"] == "reject":
        print("DANGEROUS ACTION TEST: PASS")
        tests_passed += 1
    else:
        print("DANGEROUS ACTION TEST: FAIL")

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n==========================================")
    print(f"Tests passed : {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("GLOBAL ACTION SAFETY TEST: PASS")
        print("STEP 11.14 TEST PASSED")
    else:
        print("GLOBAL ACTION SAFETY TEST: FAIL")

    print("==========================================")
    
