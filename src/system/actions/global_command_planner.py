import os
import sys


# ============================================================
# PROJECT BOOTSTRAP
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORT
# ============================================================


from src.system.actions.global_search_action_integration import (
    GlobalSearchActionIntegration,
)


# ============================================================
# GLOBAL COMMAND PLANNER
# ============================================================

class GlobalCommandPlanner:
    """
    MYX Step 11.13

    Converts a resolved global command into a SAFE action plan.

    Possible decisions:

        execute
        select
        confirm
        reject

    This module NEVER executes the action.
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

    def __init__(self, integration=None):
        self.integration = (
            integration
            if integration is not None
            else GlobalSearchActionIntegration()
        )

        print("[GlobalCommandPlanner] Initialized")

    # --------------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------------

    def normalize(self, value):
        if value is None:
            return ""

        return str(value).strip()

    # --------------------------------------------------------
    # GET ACTION
    # --------------------------------------------------------

    def get_action(self, plan):
        if not isinstance(plan, dict):
            return None

        action = plan.get("action")

        if action is None:
            return None

        return self.normalize(action).lower()

    # --------------------------------------------------------
    # GET RESULTS
    # --------------------------------------------------------

    def get_results(self, plan):
        if not isinstance(plan, dict):
            return []

        results = plan.get("results", [])

        if results is None:
            return []

        if not isinstance(results, list):
            return list(results)

        return results

    # --------------------------------------------------------
    # CLASSIFY ACTION
    # --------------------------------------------------------

    def classify_action(self, action):
        action = self.normalize(action).lower()

        if not action:
            return "reject"

        if action in self.SAFE_ACTIONS:
            return "safe"

        if action in self.CONFIRM_ACTIONS:
            return "confirm"

        return "unknown"

    # --------------------------------------------------------
    # BUILD PLAN
    # --------------------------------------------------------

    def build_plan(self, command):
        command = self.normalize(command)

        if not command:
            return {
                "success": False,
                "command": "",
                "action": None,
                "query": "",
                "decision": "reject",
                "results": [],
                "result_count": 0,
                "requires_selection": False,
                "requires_confirmation": False,
                "reason": "Empty command",
            }

        # ----------------------------------------------------
        # 11.12 INTEGRATION
        # ----------------------------------------------------

        try:
            resolved_plan = self.integration.build_action_plan(
                command
            )
        except Exception as exc:
            return {
                "success": False,
                "command": command,
                "action": None,
                "query": "",
                "decision": "reject",
                "results": [],
                "result_count": 0,
                "requires_selection": False,
                "requires_confirmation": False,
                "reason": str(exc),
            }

        if not isinstance(resolved_plan, dict):
            return {
                "success": False,
                "command": command,
                "action": None,
                "query": command,
                "decision": "reject",
                "results": [],
                "result_count": 0,
                "requires_selection": False,
                "requires_confirmation": False,
                "reason": "Invalid integration result",
            }

        action = self.get_action(resolved_plan)
        query = self.normalize(
            resolved_plan.get("query")
        )

        results = self.get_results(resolved_plan)
        result_count = len(results)

        action_type = self.classify_action(action)

        # ----------------------------------------------------
        # UNKNOWN ACTION
        # ----------------------------------------------------

        if action_type == "unknown":
            return {
                "success": False,
                "command": command,
                "action": action,
                "query": query,
                "decision": "reject",
                "results": results,
                "result_count": result_count,
                "requires_selection": False,
                "requires_confirmation": False,
                "reason": "Unknown action",
            }

        # ----------------------------------------------------
        # NO RESULTS
        # ----------------------------------------------------

        if result_count == 0:
            return {
                "success": False,
                "command": command,
                "action": action,
                "query": query,
                "decision": "reject",
                "results": [],
                "result_count": 0,
                "requires_selection": False,
                "requires_confirmation": False,
                "reason": "No matching results",
            }

        # ----------------------------------------------------
        # MULTIPLE RESULTS
        # ----------------------------------------------------

        if result_count > 1:
            return {
                "success": True,
                "command": command,
                "action": action,
                "query": query,
                "decision": "select",
                "results": results,
                "result_count": result_count,
                "requires_selection": True,
                "requires_confirmation": False,
                "reason": "Multiple matching results",
            }

        # ----------------------------------------------------
        # SINGLE SAFE RESULT
        # ----------------------------------------------------

        if action_type == "safe":
            return {
                "success": True,
                "command": command,
                "action": action,
                "query": query,
                "decision": "execute",
                "results": results,
                "result_count": 1,
                "requires_selection": False,
                "requires_confirmation": False,
                "reason": "Single safe result",
            }

        # ----------------------------------------------------
        # SINGLE CONFIRMATION ACTION
        # ----------------------------------------------------

        if action_type == "confirm":
            return {
                "success": True,
                "command": command,
                "action": action,
                "query": query,
                "decision": "confirm",
                "results": results,
                "result_count": 1,
                "requires_selection": False,
                "requires_confirmation": True,
                "reason": "Action requires confirmation",
            }

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        return {
            "success": False,
            "command": command,
            "action": action,
            "query": query,
            "decision": "reject",
            "results": results,
            "result_count": result_count,
            "requires_selection": False,
            "requires_confirmation": False,
            "reason": "Planner fallback",
        }

    # --------------------------------------------------------
    # TOP RESULT
    # --------------------------------------------------------

    def top_result(self, command):
        plan = self.build_plan(command)

        results = plan.get("results", [])

        if not results:
            return None

        if plan.get("decision") not in {
            "execute",
            "confirm",
        }:
            return None

        return results[0]

    # --------------------------------------------------------
    # CAN EXECUTE
    # --------------------------------------------------------

    def can_execute(self, command):
        plan = self.build_plan(command)

        return (
            plan.get("success") is True
            and plan.get("decision") == "execute"
        )

    # --------------------------------------------------------
    # NEEDS SELECTION
    # --------------------------------------------------------

    def needs_selection(self, command):
        plan = self.build_plan(command)

        return (
            plan.get("decision") == "select"
        )

    # --------------------------------------------------------
    # NEEDS CONFIRMATION
    # --------------------------------------------------------

    def needs_confirmation(self, command):
        plan = self.build_plan(command)

        return (
            plan.get("decision") == "confirm"
        )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    def summarize(self, command):
        plan = self.build_plan(command)

        return {
            "success": plan.get("success", False),
            "action": plan.get("action"),
            "query": plan.get("query"),
            "decision": plan.get("decision"),
            "result_count": plan.get("result_count", 0),
            "requires_selection": plan.get(
                "requires_selection",
                False,
            ),
            "requires_confirmation": plan.get(
                "requires_confirmation",
                False,
            ),
        }

    # --------------------------------------------------------
    # PRINT PLAN
    # --------------------------------------------------------

    def print_plan(self, command):
        plan = self.build_plan(command)

        print("\n==========================================")
        print("MYX GLOBAL COMMAND PLAN")
        print("==========================================")

        print("Command :", plan.get("command"))
        print("Action  :", plan.get("action"))
        print("Query   :", plan.get("query"))
        print("Decision:", plan.get("decision"))
        print("Results :", plan.get("result_count"))

        print(
            "Selection Required    :",
            plan.get("requires_selection"),
        )

        print(
            "Confirmation Required :",
            plan.get("requires_confirmation"),
        )

        print("Reason  :", plan.get("reason"))

        print("\nResults:")

        for index, result in enumerate(
            plan.get("results", [])[:10],
            start=1,
        ):
            if isinstance(result, dict):
                name = result.get(
                    "name",
                    result.get(
                        "title",
                        "Unknown",
                    ),
                )

                path = result.get(
                    "path",
                    result.get(
                        "launch_target",
                        "",
                    ),
                )

                print(f"{index}. {name}")

                if path:
                    print(f"   {path}")

            else:
                print(f"{index}. {result}")

        print("==========================================")

        return plan


# ============================================================
# MOCK INTEGRATION
# ============================================================

class MockIntegration:
    """
    Controlled integration for testing.

    No real system operation is performed.
    """

    def __init__(self):
        self.records = [
            {
                "name": "Google Chrome",
                "path": r"C:\Program Files\Google\Chrome\chrome.exe",
                "type": "application",
            },
            {
                "name": "Chrome Project",
                "path": r"C:\Users\AVISHKAR\Projects\Chrome Project",
                "type": "folder",
            },
        ]

    def build_action_plan(self, command):
        command = str(command).strip()

        if not command:
            return {
                "success": False,
                "action": None,
                "query": "",
                "results": [],
            }

        lower = command.lower()

        if lower.startswith("find "):
            query = command[5:].strip()

            return {
                "success": True,
                "action": "find",
                "query": query,
                "results": self.records,
                "result_count": len(self.records),
            }

        if lower.startswith("search "):
            query = command[7:].strip()

            return {
                "success": True,
                "action": "search",
                "query": query,
                "results": [
                    self.records[0]
                ],
                "result_count": 1,
            }

        if lower.startswith("open "):
            query = command[5:].strip()

            return {
                "success": True,
                "action": "open",
                "query": query,
                "results": [
                    self.records[0]
                ],
                "result_count": 1,
            }

        return {
            "success": False,
            "action": None,
            "query": command,
            "results": [],
        }


# ============================================================
# TEST 1 — INITIALIZATION
# ============================================================

def test_initialization():
    planner = GlobalCommandPlanner(
        integration=MockIntegration()
    )

    assert planner.integration is not None

    print("INITIALIZATION TEST: PASS")


# ============================================================
# TEST 2 — SAFE SINGLE RESULT
# ============================================================

def test_safe_single_result():
    planner = GlobalCommandPlanner(
        integration=MockIntegration()
    )

    plan = planner.build_plan(
        "search chrome"
    )

    assert plan["success"] is True
    assert plan["decision"] == "execute"
    assert plan["requires_confirmation"] is False

    print("SAFE SINGLE RESULT TEST: PASS")


# ============================================================
# TEST 3 — MULTIPLE RESULT SELECTION
# ============================================================

def test_multiple_results():
    planner = GlobalCommandPlanner(
        integration=MockIntegration()
    )

    plan = planner.build_plan(
        "find chrome"
    )

    assert plan["success"] is True
    assert plan["decision"] == "select"
    assert plan["requires_selection"] is True
    assert plan["result_count"] == 2

    print("MULTIPLE RESULT TEST: PASS")


# ============================================================
# TEST 4 — CONFIRMATION REQUIRED
# ============================================================

def test_confirmation():
    planner = GlobalCommandPlanner(
        integration=MockIntegration()
    )

    plan = planner.build_plan(
        "open chrome"
    )

    assert plan["success"] is True
    assert plan["decision"] == "confirm"
    assert plan["requires_confirmation"] is True

    print("CONFIRMATION TEST: PASS")


# ============================================================
# TEST 5 — EMPTY COMMAND
# ============================================================

def test_empty_command():
    planner = GlobalCommandPlanner(
        integration=MockIntegration()
    )

    plan = planner.build_plan("")

    assert plan["success"] is False
    assert plan["decision"] == "reject"
    assert plan["result_count"] == 0

    print("EMPTY COMMAND SAFETY TEST: PASS")


# ============================================================
# TEST 6 — UNKNOWN ACTION
# ============================================================

def test_unknown_action():
    planner = GlobalCommandPlanner(
        integration=MockIntegration()
    )

    class UnknownIntegration:

        def build_action_plan(self, command):
            return {
                "success": True,
                "action": "delete_everything",
                "query": "test",
                "results": [
                    {
                        "name": "Test",
                        "path": r"C:\Test",
                    }
                ],
            }

    planner = GlobalCommandPlanner(
        integration=UnknownIntegration()
    )

    plan = planner.build_plan(
        "delete everything"
    )

    assert plan["success"] is False
    assert plan["decision"] == "reject"

    print("UNKNOWN ACTION SAFETY TEST: PASS")


# ============================================================
# TEST 7 — TOP RESULT SAFETY
# ============================================================

def test_top_result():
    planner = GlobalCommandPlanner(
        integration=MockIntegration()
    )

    result = planner.top_result(
        "search chrome"
    )

    assert result is not None
    assert result["name"] == "Google Chrome"

    # Multiple results must NOT automatically return a target.
    result_multiple = planner.top_result(
        "find chrome"
    )

    assert result_multiple is None

    print("TOP RESULT SAFETY TEST: PASS")


# ============================================================
# TEST 8 — DECISION HELPERS
# ============================================================

def test_decision_helpers():
    planner = GlobalCommandPlanner(
        integration=MockIntegration()
    )

    assert planner.can_execute(
        "search chrome"
    ) is True

    assert planner.needs_selection(
        "find chrome"
    ) is True

    assert planner.needs_confirmation(
        "open chrome"
    ) is True

    print("DECISION HELPERS TEST: PASS")


# ============================================================
# MAIN TEST RUNNER
# ============================================================

if __name__ == "__main__":

    print("\n==========================================")
    print("MYX STEP 11.13 COMMAND PLANNER TEST")
    print("==========================================")

    tests = [
        test_initialization,
        test_safe_single_result,
        test_multiple_results,
        test_confirmation,
        test_empty_command,
        test_unknown_action,
        test_top_result,
        test_decision_helpers,
    ]

    passed = 0

    for test in tests:
        try:
            test()
            passed += 1

        except Exception as exc:
            print(
                f"{test.__name__.upper()}: FAIL"
            )
            print("Reason:", exc)

    print("\n==========================================")
    print(
        f"Tests passed : {passed}/{len(tests)}"
    )

    if passed == len(tests):
        print("COMMAND PLANNER TEST: PASS")
        print("STEP 11.13 TEST PASSED")
    else:
        print("COMMAND PLANNER TEST: FAIL")
        print("STEP 11.13 TEST FAILED")

    print("==========================================")
    
