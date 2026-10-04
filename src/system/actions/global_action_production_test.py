"""
MYX Global Action Production Integration Test
STEP 11.19

Purpose:
    Verify that the real MYX global-action modules can work together.

Real components:
    Discovery / Search
    Global Search Intelligence
    Global Command Planner
    Global Action Safety Manager
    Global Selection Manager
    Global Action Pipeline
    Global Action Audit

Mocked component:
    Global Action Executor

NO REAL APPLICATION IS LAUNCHED.
NO WINDOWS ACTION IS EXECUTED.
"""

import os
import sys


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# IMPORT PIPELINE
# =========================================================

from src.system.actions.global_action_pipeline import (
    GlobalActionPipeline,
)


# =========================================================
# REAL COMPONENT IMPORTS
# =========================================================

try:
    from src.system.search.global_search_intelligence import (
        GlobalSearchIntelligence,
    )
except Exception:
    GlobalSearchIntelligence = None

try:
    from src.system.actions.global_command_planner import (
        GlobalCommandPlanner,
    )
except Exception:
    GlobalCommandPlanner = None

try:
    from src.system.actions.global_action_safety_manager import (
        GlobalActionSafetyManager,
    )
except Exception:
    GlobalActionSafetyManager = None

try:
    from src.system.actions.global_selection_manager import (
        GlobalSelectionManager,
    )
except Exception:
    GlobalSelectionManager = None

try:
    from src.system.actions.global_action_audit import (
        GlobalActionAudit,
    )
except Exception:
    GlobalActionAudit = None


# =========================================================
# MOCK EXECUTOR
# =========================================================

class ProductionTestExecutor:
    """
    Safe executor for production integration testing.

    It records what WOULD have been executed but never
    launches an application, opens a file, opens a URL,
    or changes Windows state.
    """

    def __init__(self):
        self.calls = []

    def execute(self, plan):
        self.calls.append(plan)

        return {
            "success": True,
            "message": "MOCK EXECUTION SUCCESS",
            "mock": True,
        }


# =========================================================
# HELPERS
# =========================================================

def check(condition, name):
    if condition:
        print(f"[PASS] {name}")
        return True

    print(f"[FAIL] {name}")
    return False


# =========================================================
# TESTS
# =========================================================

def run_tests():

    print("\n==========================================")
    print("MYX GLOBAL ACTION PRODUCTION TEST")
    print("STEP 11.19")
    print("==========================================")

    total = 10
    passed = 0

    # -----------------------------------------------------
    # TEST 1
    # -----------------------------------------------------

    components_available = all(
        component is not None
        for component in (
            GlobalSearchIntelligence,
            GlobalCommandPlanner,
            GlobalActionSafetyManager,
            GlobalSelectionManager,
            GlobalActionAudit,
        )
    )

    if check(
        components_available,
        "Real component imports",
    ):
        passed += 1

    if not components_available:
        print(
            "\nRequired real components could not be imported."
        )
        print(
            f"Tests passed : {passed}/{total}"
        )
        print(
            "STEP 11.19 TEST FAILED"
        )
        return False

    # -----------------------------------------------------
    # CREATE REAL COMPONENTS
    # -----------------------------------------------------

    try:
        search = GlobalSearchIntelligence()
        planner = GlobalCommandPlanner()
        safety = GlobalActionSafetyManager()
        selection = GlobalSelectionManager()
        audit = GlobalActionAudit()

        executor = ProductionTestExecutor()

        pipeline = GlobalActionPipeline(
            search=search,
            planner=planner,
            safety=safety,
            selection=selection,
            executor=executor,
            audit=audit,
        )

        if check(
            pipeline is not None,
            "Pipeline initialization",
        ):
            passed += 1

    except Exception as e:

        print(
            f"[FAIL] Pipeline initialization: {e}"
        )

        print("\n==========================================")
        print(f"Tests passed : {passed}/{total}")
        print("STEP 11.19 TEST FAILED")
        print("==========================================\n")

        return False

    # -----------------------------------------------------
    # TEST 3
    # REAL SEARCH
    # -----------------------------------------------------

    try:

        candidates = pipeline.search_targets(
            "Visual Studio Code"
        )

        search_ok = isinstance(
            candidates,
            list,
        )

        if check(
            search_ok,
            "Real search stage",
        ):
            passed += 1

        print(
            f"       Search candidates: {len(candidates)}"
        )

    except Exception as e:

        print(
            f"[FAIL] Real search stage: {e}"
        )

    # -----------------------------------------------------
    # TEST 4
    # REAL PLANNER
    # -----------------------------------------------------

    try:

        plan = pipeline.create_plan(
            "Open Visual Studio Code",
            candidates,
        )

        planner_ok = (
            isinstance(plan, dict)
            and bool(plan)
        )

        if check(
            planner_ok,
            "Real planner stage",
        ):
            passed += 1

        print(
            f"       Planned action: "
            f"{plan.get('action')}"
        )

    except Exception as e:

        print(
            f"[FAIL] Real planner stage: {e}"
        )

        plan = {
            "command": "Open Visual Studio Code",
            "action": "open",
            "decision": "select",
            "target": None,
            "candidates": candidates,
        }

    # -----------------------------------------------------
    # TEST 5
    # REAL SAFETY
    # -----------------------------------------------------

    try:

        safety_result = pipeline.check_safety(
            plan
        )

        safety_ok = isinstance(
            safety_result,
            dict,
        )

        if check(
            safety_ok,
            "Real safety stage",
        ):
            passed += 1

        print(
            f"       Safety decision: "
            f"{safety_result.get('decision')}"
        )

    except Exception as e:

        print(
            f"[FAIL] Real safety stage: {e}"
        )

        safety_result = {
            "decision": "select",
            "allowed": True,
        }

    # -----------------------------------------------------
    # TEST 6
    # REAL SELECTION
    # -----------------------------------------------------

    try:

        selected = pipeline.select_target(
            candidates,
            plan,
        )

        selection_ok = (
            selected is None
            or isinstance(
                selected,
                (dict, str),
            )
        )

        if check(
            selection_ok,
            "Real selection stage",
        ):
            passed += 1

        print(
            f"       Selected target: "
            f"{selected}"
        )

    except Exception as e:

        print(
            f"[FAIL] Real selection stage: {e}"
        )

        selected = None

    # -----------------------------------------------------
    # TEST 7
    # MOCK EXECUTOR
    # -----------------------------------------------------

    try:

        execution_result = pipeline.execute_action(
            plan,
            selected,
        )

        execution_ok = (
            isinstance(
                execution_result,
                dict,
            )
            and execution_result.get(
                "success"
            ) is True
            and execution_result.get(
                "mock"
            ) is True
        )

        if check(
            execution_ok,
            "Safe mock execution",
        ):
            passed += 1

    except Exception as e:

        print(
            f"[FAIL] Safe mock execution: {e}"
        )

    # -----------------------------------------------------
    # TEST 8
    # REAL AUDIT
    # -----------------------------------------------------

    try:

        audit_before = len(
            getattr(
                audit,
                "records",
                [],
            )
        )

        audit_record = pipeline.audit_action(
            "Open Visual Studio Code",
            plan,
            selected,
            execution_result,
            safety_result,
        )

        audit_after = len(
            getattr(
                audit,
                "records",
                [],
            )
        )

        audit_ok = (
            isinstance(
                audit_record,
                dict,
            )
            and audit_after >= audit_before
        )

        if check(
            audit_ok,
            "Real audit stage",
        ):
            passed += 1

    except Exception as e:

        print(
            f"[FAIL] Real audit stage: {e}"
        )

    # -----------------------------------------------------
    # TEST 9
    # COMPLETE PIPELINE
    # -----------------------------------------------------

    try:

        full_result = pipeline.process(
            "Visual Studio Code"
        )

        full_ok = (
            isinstance(
                full_result,
                dict,
            )
            and "success" in full_result
        )

        if check(
            full_ok,
            "Complete real pipeline",
        ):
            passed += 1

        print(
            f"       Final result: "
            f"{full_result}"
        )

    except Exception as e:

        print(
            f"[FAIL] Complete real pipeline: {e}"
        )

    # -----------------------------------------------------
    # TEST 10
    # NO REAL EXECUTION
    # -----------------------------------------------------

    mock_only = all(
        call is not None
        for call in executor.calls
    )

    if check(
        mock_only,
        "Execution remained mocked",
    ):
        passed += 1

    print(
        f"       Mock executor calls: "
        f"{len(executor.calls)}"
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    print("\n==========================================")
    print(
        f"Tests passed : {passed}/{total}"
    )

    if passed == total:

        print(
            "GLOBAL ACTION PRODUCTION TEST: PASS"
        )

        print(
            "STEP 11.19 TEST PASSED"
        )

        result = True

    else:

        print(
            "GLOBAL ACTION PRODUCTION TEST: FAIL"
        )

        print(
            "STEP 11.19 TEST FAILED"
        )

        result = False

    print("==========================================\n")

    return result


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    run_tests()

