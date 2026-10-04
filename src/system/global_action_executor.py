import os
import sys
import subprocess
import webbrowser


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
# GLOBAL ACTION EXECUTOR
# ============================================================

class GlobalActionExecutor:
    """
    MYX Global Action Executor

    Responsible for executing only decisions that have already
    passed through the safety/planning layers.

    Supported decisions:
        execute
        confirm
        select
        reject

    This module does NOT interpret natural-language commands.
    It only executes an already-resolved action plan.
    """

    EXECUTABLE_ACTIONS = {
        "find",
        "search",
        "locate",
        "show",
        "open",
        "launch",
        "start",
        "run",
    }

    def __init__(self):
        print("[GlobalActionExecutor] Initialized")

    # ========================================================
    # BASIC HELPERS
    # ========================================================

    def normalize(self, value):
        if value is None:
            return ""

        return str(value).strip()

    def get_decision(self, plan):
        if not isinstance(plan, dict):
            return ""

        return self.normalize(
            plan.get("decision", "")
        ).lower()

    def get_action(self, plan):
        if not isinstance(plan, dict):
            return ""

        return self.normalize(
            plan.get("action", "")
        ).lower()

    def get_target(self, plan):
        if not isinstance(plan, dict):
            return None

        if "target" in plan:
            return plan.get("target")

        if "result" in plan:
            return plan.get("result")

        if "selected_candidate" in plan:
            return plan.get("selected_candidate")

        return None

    # ========================================================
    # TARGET EXTRACTION
    # ========================================================

    def extract_target_path(self, target):
        if target is None:
            return None

        if isinstance(target, str):
            return target.strip()

        if not isinstance(target, dict):
            return None

        possible_keys = [
            "path",
            "full_path",
            "launch_target",
            "target",
            "executable",
            "file_path",
            "location",
        ]

        for key in possible_keys:
            value = target.get(key)

            if value:
                value = self.normalize(value)

                if value:
                    return value

        return None

    def extract_target_url(self, target):
        if target is None:
            return None

        if isinstance(target, str):
            value = target.strip()

            if value.lower().startswith(
                ("http://", "https://")
            ):
                return value

            return None

        if not isinstance(target, dict):
            return None

        possible_keys = [
            "url",
            "launch_target",
            "target",
        ]

        for key in possible_keys:
            value = target.get(key)

            if not value:
                continue

            value = self.normalize(value)

            if value.lower().startswith(
                ("http://", "https://")
            ):
                return value

        return None

    # ========================================================
    # FILE / FOLDER EXECUTION
    # ========================================================

    def open_path(self, path):
        path = self.normalize(path)

        if not path:
            return {
                "success": False,
                "method": "path",
                "message": "No path supplied.",
            }

        if not os.path.exists(path):
            return {
                "success": False,
                "method": "path",
                "target": path,
                "message": "Target path does not exist.",
            }

        try:
            os.startfile(path)

            return {
                "success": True,
                "method": "path",
                "target": path,
                "message": f"Opened {path}",
            }

        except Exception as exc:
            return {
                "success": False,
                "method": "path",
                "target": path,
                "message": f"Unable to open path: {exc}",
            }

    # ========================================================
    # URL EXECUTION
    # ========================================================

    def open_url(self, url):
        url = self.normalize(url)

        if not url:
            return {
                "success": False,
                "method": "url",
                "message": "No URL supplied.",
            }

        if not url.lower().startswith(
            ("http://", "https://")
        ):
            return {
                "success": False,
                "method": "url",
                "target": url,
                "message": "Invalid URL.",
            }

        try:
            webbrowser.open(url)

            return {
                "success": True,
                "method": "url",
                "target": url,
                "message": f"Opened {url}",
            }

        except Exception as exc:
            return {
                "success": False,
                "method": "url",
                "target": url,
                "message": f"Unable to open URL: {exc}",
            }

    # ========================================================
    # EXECUTABLE EXECUTION
    # ========================================================

    def launch_executable(self, executable):
        executable = self.normalize(executable)

        if not executable:
            return {
                "success": False,
                "method": "executable",
                "message": "No executable supplied.",
            }

        try:
            subprocess.Popen(
                executable,
                shell=False
            )

            return {
                "success": True,
                "method": "executable",
                "target": executable,
                "message": f"Launched {executable}",
            }

        except FileNotFoundError:
            return {
                "success": False,
                "method": "executable",
                "target": executable,
                "message": "Executable was not found.",
            }

        except Exception as exc:
            return {
                "success": False,
                "method": "executable",
                "target": executable,
                "message": f"Unable to launch executable: {exc}",
            }

    # ========================================================
    # APP ID EXECUTION
    # ========================================================

    def launch_app_id(self, app_id):
        app_id = self.normalize(app_id)

        if not app_id:
            return {
                "success": False,
                "method": "app_id",
                "message": "No App ID supplied.",
            }

        try:
            command = [
                "explorer.exe",
                f"shell:AppsFolder\\{app_id}"
            ]

            subprocess.Popen(command)

            return {
                "success": True,
                "method": "app_id",
                "target": app_id,
                "message": f"Launched application {app_id}",
            }

        except Exception as exc:
            return {
                "success": False,
                "method": "app_id",
                "target": app_id,
                "message": f"Unable to launch application: {exc}",
            }

    # ========================================================
    # TARGET TYPE DETECTION
    # ========================================================

    def execute_target(self, target):
        if target is None:
            return {
                "success": False,
                "method": "none",
                "message": "No execution target available.",
            }

        # ----------------------------------------------------
        # String target
        # ----------------------------------------------------

        if isinstance(target, str):
            value = target.strip()

            if not value:
                return {
                    "success": False,
                    "method": "string",
                    "message": "Empty target.",
                }

            if value.lower().startswith(
                ("http://", "https://")
            ):
                return self.open_url(value)

            if os.path.exists(value):
                return self.open_path(value)

            return self.launch_executable(value)

        # ----------------------------------------------------
        # Dictionary target
        # ----------------------------------------------------

        if not isinstance(target, dict):
            return {
                "success": False,
                "method": "unknown",
                "message": "Unsupported target format.",
            }

        # URL
        url = self.extract_target_url(target)

        if url:
            return self.open_url(url)

        # Existing filesystem path
        path = self.extract_target_path(target)

        if path:
            if path.lower().startswith(
                ("http://", "https://")
            ):
                return self.open_url(path)

            if os.path.exists(path):
                return self.open_path(path)

        # Executable
        executable = target.get("executable")

        if executable:
            return self.launch_executable(executable)

        # App ID
        app_id = target.get("app_id")

        if app_id:
            return self.launch_app_id(app_id)

        return {
            "success": False,
            "method": "unknown",
            "message": "No executable target could be resolved.",
        }

    # ========================================================
    # PLAN EXECUTION
    # ========================================================

    def execute_plan(self, plan, confirmed=False):
        """
        Execute an already planned action.

        Rules:
            execute  -> execute immediately
            select   -> do not execute
            confirm  -> execute only when confirmed=True
            reject   -> never execute
        """

        if not isinstance(plan, dict):
            return {
                "success": False,
                "decision": "reject",
                "message": "Invalid action plan.",
            }

        decision = self.get_decision(plan)
        action = self.get_action(plan)
        target = self.get_target(plan)

        # ----------------------------------------------------
        # REJECT
        # ----------------------------------------------------

        if decision == "reject":
            return {
                "success": False,
                "decision": "reject",
                "action": action,
                "message": "Action rejected by safety layer.",
            }

        # ----------------------------------------------------
        # SELECT
        # ----------------------------------------------------

        if decision == "select":
            return {
                "success": False,
                "decision": "select",
                "action": action,
                "message": "User selection is required before execution.",
            }

        # ----------------------------------------------------
        # CONFIRM
        # ----------------------------------------------------

        if decision == "confirm" and not confirmed:
            return {
                "success": False,
                "decision": "confirm",
                "action": action,
                "message": "User confirmation is required.",
            }

        # ----------------------------------------------------
        # UNKNOWN DECISION
        # ----------------------------------------------------

        if decision not in {
            "execute",
            "confirm",
        }:
            return {
                "success": False,
                "decision": "reject",
                "action": action,
                "message": "Unknown execution decision.",
            }

        # ----------------------------------------------------
        # ACTION VALIDATION
        # ----------------------------------------------------

        if action not in self.EXECUTABLE_ACTIONS:
            return {
                "success": False,
                "decision": decision,
                "action": action,
                "message": "Action is not executable.",
            }

        # ----------------------------------------------------
        # TARGET EXECUTION
        # ----------------------------------------------------

        result = self.execute_target(target)

        result["decision"] = decision
        result["action"] = action

        return result

    # ========================================================
    # SAFE EXECUTION ENTRY
    # ========================================================

    def execute(self, plan, confirmed=False):
        return self.execute_plan(
            plan,
            confirmed=confirmed
        )


# ============================================================
# STEP 11.16 TESTS
# ============================================================

def run_tests():

    print()
    print("MYX STEP 11.16 GLOBAL ACTION EXECUTOR TEST")
    print("=" * 55)

    executor = GlobalActionExecutor()

    passed = 0
    total = 8

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    print("[TEST 1] Executor Initialization")

    if isinstance(executor, GlobalActionExecutor):
        print("EXECUTOR INIT TEST: PASS")
        passed += 1
    else:
        print("EXECUTOR INIT TEST: FAIL")

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    print("[TEST 2] Reject Decision Safety")

    plan = {
        "decision": "reject",
        "action": "delete",
        "target": "test.txt",
    }

    result = executor.execute(plan)

    if (
        result.get("success") is False
        and result.get("decision") == "reject"
    ):
        print("REJECT SAFETY TEST: PASS")
        passed += 1
    else:
        print("REJECT SAFETY TEST: FAIL")

    # --------------------------------------------------------
    # TEST 3
    # --------------------------------------------------------

    print("[TEST 3] Selection Safety")

    plan = {
        "decision": "select",
        "action": "open",
        "target": "test.txt",
    }

    result = executor.execute(plan)

    if (
        result.get("success") is False
        and result.get("decision") == "select"
    ):
        print("SELECTION SAFETY TEST: PASS")
        passed += 1
    else:
        print("SELECTION SAFETY TEST: FAIL")

    # --------------------------------------------------------
    # TEST 4
    # --------------------------------------------------------

    print("[TEST 4] Confirmation Safety")

    plan = {
        "decision": "confirm",
        "action": "open",
        "target": "test.txt",
    }

    result = executor.execute(plan)

    if (
        result.get("success") is False
        and result.get("decision") == "confirm"
    ):
        print("CONFIRMATION SAFETY TEST: PASS")
        passed += 1
    else:
        print("CONFIRMATION SAFETY TEST: FAIL")

    # --------------------------------------------------------
    # TEST 5
    # --------------------------------------------------------

    print("[TEST 5] Unknown Decision Safety")

    plan = {
        "decision": "something_unknown",
        "action": "open",
        "target": "test.txt",
    }

    result = executor.execute(plan)

    if result.get("success") is False:
        print("UNKNOWN DECISION TEST: PASS")
        passed += 1
    else:
        print("UNKNOWN DECISION TEST: FAIL")

    # --------------------------------------------------------
    # TEST 6
    # --------------------------------------------------------

    print("[TEST 6] Empty Target Safety")

    plan = {
        "decision": "execute",
        "action": "open",
        "target": None,
    }

    result = executor.execute(plan)

    if result.get("success") is False:
        print("EMPTY TARGET TEST: PASS")
        passed += 1
    else:
        print("EMPTY TARGET TEST: FAIL")

    # --------------------------------------------------------
    # TEST 7
    # --------------------------------------------------------

    print("[TEST 7] Mocked Target Execution")

    original_execute_target = executor.execute_target

    try:

        executor.execute_target = lambda target: {
            "success": True,
            "method": "mock",
            "target": target,
            "message": "Mock execution successful.",
        }

        plan = {
            "decision": "execute",
            "action": "open",
            "target": {
                "name": "Google Chrome"
            },
        }

        result = executor.execute(plan)

        if (
            result.get("success") is True
            and result.get("decision") == "execute"
            and result.get("action") == "open"
        ):
            print("MOCK EXECUTION TEST: PASS")
            passed += 1
        else:
            print("MOCK EXECUTION TEST: FAIL")

    finally:
        executor.execute_target = original_execute_target

    # --------------------------------------------------------
    # TEST 8
    # --------------------------------------------------------

    print("[TEST 8] Confirmed Execution")

    original_execute_target = executor.execute_target

    try:

        executor.execute_target = lambda target: {
            "success": True,
            "method": "mock",
            "target": target,
            "message": "Confirmed mock execution.",
        }

        plan = {
            "decision": "confirm",
            "action": "launch",
            "target": {
                "name": "Calculator"
            },
        }

        result = executor.execute(
            plan,
            confirmed=True
        )

        if (
            result.get("success") is True
            and result.get("decision") == "confirm"
        ):
            print("CONFIRMED EXECUTION TEST: PASS")
            passed += 1
        else:
            print("CONFIRMED EXECUTION TEST: FAIL")

    finally:
        executor.execute_target = original_execute_target

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print()
    print(f"Tests passed : {passed}/{total}")

    if passed == total:
        print("GLOBAL ACTION EXECUTOR TEST: PASS")
        print("STEP 11.16 TEST PASSED")
    else:
        print("GLOBAL ACTION EXECUTOR TEST: FAIL")
        print("STEP 11.16 TEST FAILED")

    print("=" * 55)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run_tests()
