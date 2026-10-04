# ============================================================
# MYX GLOBAL ACTION EXECUTOR
# PRODUCTION CLEAN VERSION
#
# Responsibility:
#   Execute already-approved action plans.
#
# Architecture:
#   Plan
#     ↓
#   Target Adapter
#     ↓
#   Target Normalization
#     ↓
#   Windows Execution
#     ↓
#   Structured Result
#
# This module does NOT understand natural language.
# ============================================================

from __future__ import annotations

import os
import subprocess
import webbrowser
from typing import Any


class GlobalActionExecutor:
    """
    MYX Global Action Executor.

    Executes targets that have already passed:
        Search
        Planning
        Safety
        Selection

    Supported actions:
        find
        search
        locate
        show
        open
        launch
        start
        run
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

    @staticmethod
    def normalize(value: Any) -> str:
        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def get_decision(plan: dict) -> str:
        if not isinstance(plan, dict):
            return ""

        return GlobalActionExecutor.normalize(
            plan.get("decision", "")
        ).lower()

    @staticmethod
    def get_action(plan: dict) -> str:
        if not isinstance(plan, dict):
            return ""

        return GlobalActionExecutor.normalize(
            plan.get("action", "")
        ).lower()

    # ========================================================
    # TARGET EXTRACTION
    # ========================================================

    def get_target(self, plan: dict):
        if not isinstance(plan, dict):
            return None

        for key in (
            "target",
            "selected_target",
            "selected_candidate",
            "result",
        ):
            if key in plan and plan.get(key) is not None:
                return plan.get(key)

        return None

    # ========================================================
    # DISCOVERY RECORD ADAPTER
    # ========================================================

    def target_to_dict(self, target) -> dict | None:
        """
        Convert any supported MYX discovery target into
        a normalized dictionary.

        Supports:
            dict
            DiscoveryRecord
            normal Python objects with attributes
        """

        if target is None:
            return None

        # Already normalized
        if isinstance(target, dict):
            return dict(target)

        # ----------------------------------------------------
        # Generic object / DiscoveryRecord
        # ----------------------------------------------------

        data = {}

        possible_fields = (
            "name",
            "normalized_name",
            "item_type",
            "source",
            "location",
            "target",
            "executable",
            "launchable",
            "capabilities",
            "metadata",
            "app_id",
            "url",
            "path",
            "full_path",
            "file_path",
            "launch_target",
        )

        for field in possible_fields:
            try:
                if hasattr(target, field):
                    value = getattr(target, field)

                    if value is not None:
                        data[field] = value
            except Exception:
                continue

        # ----------------------------------------------------
        # Dataclass-style objects
        # ----------------------------------------------------

        if not data and hasattr(target, "__dict__"):
            try:
                raw = vars(target)

                if isinstance(raw, dict):
                    data.update(raw)
            except Exception:
                pass

        if not data:
            return None

        return data

    # ========================================================
    # TARGET TYPE
    # ========================================================

    def get_item_type(self, target_data: dict) -> str:
        value = target_data.get(
            "item_type",
            target_data.get("type", ""),
        )

        return self.normalize(value).lower()

    # ========================================================
    # TARGET PATH
    # ========================================================

    def extract_target_path(self, target_data: dict):
        if not isinstance(target_data, dict):
            return None

        possible_keys = (
            "path",
            "full_path",
            "file_path",
            "location",
        )

        for key in possible_keys:
            value = target_data.get(key)

            if value:
                value = self.normalize(value)

                if value:
                    return value

        # Some records use "target" for filesystem path
        value = target_data.get("target")

        if value:
            value = self.normalize(value)

            if value and (
                os.path.exists(value)
                or "\\" in value
                or "/" in value
            ):
                return value

        return None

    # ========================================================
    # URL
    # ========================================================

    def extract_target_url(self, target_data: dict):
        if not isinstance(target_data, dict):
            return None

        for key in (
            "url",
            "launch_target",
            "target",
        ):
            value = target_data.get(key)

            if not value:
                continue

            value = self.normalize(value)

            if value.lower().startswith(
                (
                    "http://",
                    "https://",
                )
            ):
                return value

        return None

    # ========================================================
    # APPLICATION ID
    # ========================================================

    def extract_app_id(self, target_data: dict):
        if not isinstance(target_data, dict):
            return None

        app_id = target_data.get("app_id")

        if app_id:
            return self.normalize(app_id)

        metadata = target_data.get("metadata")

        if isinstance(metadata, dict):
            app_id = metadata.get("app_id")

            if app_id:
                return self.normalize(app_id)

        return None

    # ========================================================
    # EXECUTABLE
    # ========================================================

    def extract_executable(self, target_data: dict):
        if not isinstance(target_data, dict):
            return None

        for key in (
            "executable",
            "launch_target",
        ):
            value = target_data.get(key)

            if value:
                value = self.normalize(value)

                if value:
                    return value

        return None

    # ========================================================
    # WINDOWS PATH OPEN
    # ========================================================

    def open_path(self, path: str):
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
    # URL
    # ========================================================

    def open_url(self, url: str):
        url = self.normalize(url)

        if not url:
            return {
                "success": False,
                "method": "url",
                "message": "No URL supplied.",
            }

        if not url.lower().startswith(
            (
                "http://",
                "https://",
            )
        ):
            return {
                "success": False,
                "method": "url",
                "target": url,
                "message": "Invalid URL.",
            }

        try:
            opened = webbrowser.open(url)

            return {
                "success": bool(opened),
                "method": "url",
                "target": url,
                "message": (
                    f"Opened {url}"
                    if opened
                    else f"Unable to open {url}"
                ),
            }

        except Exception as exc:
            return {
                "success": False,
                "method": "url",
                "target": url,
                "message": f"Unable to open URL: {exc}",
            }

    # ========================================================
    # EXECUTABLE
    # ========================================================

    def launch_executable(self, executable: str):
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
                shell=False,
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
    # WINDOWS APP ID
    # ========================================================

    def launch_app_id(self, app_id: str):
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
                f"shell:AppsFolder\\{app_id}",
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
    # NORMALIZED TARGET EXECUTION
    # ========================================================

    def execute_normalized_target(self, target_data: dict):
        """
        Execute a normalized target dictionary.
        """

        if not target_data:
            return {
                "success": False,
                "method": "target",
                "message": "Target could not be normalized.",
            }

        # ----------------------------------------------------
        # URL
        # ----------------------------------------------------

        url = self.extract_target_url(target_data)

        if url:
            return self.open_url(url)

        # ----------------------------------------------------
        # Application
        # ----------------------------------------------------

        item_type = self.get_item_type(target_data)

        app_id = self.extract_app_id(target_data)

        if (
            item_type in {
                "application",
                "app",
                "program",
            }
            and app_id
        ):
            return self.launch_app_id(app_id)

        # ----------------------------------------------------
        # Existing filesystem target
        # ----------------------------------------------------

        path = self.extract_target_path(target_data)

        if path:
            if path.lower().startswith(
                (
                    "http://",
                    "https://",
                )
            ):
                return self.open_url(path)

            if os.path.exists(path):
                return self.open_path(path)

        # ----------------------------------------------------
        # Explicit executable
        # ----------------------------------------------------

        executable = self.extract_executable(target_data)

        if executable:
            if os.path.exists(executable):
                return self.open_path(executable)

            return self.launch_executable(executable)

        # ----------------------------------------------------
        # Application target fallback
        # ----------------------------------------------------

        if item_type in {
            "application",
            "app",
            "program",
        }:

            # Windows may expose launch target through metadata
            metadata = target_data.get("metadata")

            if isinstance(metadata, dict):

                for key in (
                    "launch_target",
                    "executable",
                    "path",
                ):
                    value = metadata.get(key)

                    if value:
                        value = self.normalize(value)

                        if os.path.exists(value):
                            return self.open_path(value)

                        return self.launch_executable(value)

        return {
            "success": False,
            "method": "unknown",
            "message": (
                "No executable target could be resolved."
            ),
        }

    # ========================================================
    # TARGET EXECUTION
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
                (
                    "http://",
                    "https://",
                )
            ):
                return self.open_url(value)

            if os.path.exists(value):
                return self.open_path(value)

            return self.launch_executable(value)

        # ----------------------------------------------------
        # Any object → dictionary
        # ----------------------------------------------------

        target_data = self.target_to_dict(target)

        if target_data is None:
            return {
                "success": False,
                "method": "target_adapter",
                "message": "Unsupported target format.",
            }

        return self.execute_normalized_target(
            target_data
        )

    # ========================================================
    # PLAN EXECUTION
    # ========================================================

    def execute_plan(
        self,
        plan,
        confirmed=False,
    ):
        """
        Execute an already approved plan.
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
                "message": (
                    "User selection is required "
                    "before execution."
                ),
            }

        # ----------------------------------------------------
        # CONFIRM
        # ----------------------------------------------------

        if decision == "confirm" and not confirmed:
            return {
                "success": False,
                "decision": "confirm",
                "action": action,
                "message": (
                    "User confirmation is required."
                ),
            }

        # ----------------------------------------------------
        # DECISION VALIDATION
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

        if not isinstance(result, dict):
            result = {
                "success": bool(result),
                "message": str(result),
            }

        result.setdefault(
            "decision",
            decision,
        )

        result.setdefault(
            "action",
            action,
        )

        return result

    # ========================================================
    # PUBLIC EXECUTION API
    # ========================================================

    def execute(
        self,
        plan,
        confirmed=False,
    ):
        return self.execute_plan(
            plan,
            confirmed=confirmed,
        )


# ============================================================
# ISOLATED TESTS
# ============================================================

def run_tests():

    print()
    print("=" * 64)
    print("MYX GLOBAL ACTION EXECUTOR TEST")
    print("PRODUCTION CLEAN VERSION")
    print("=" * 64)

    executor = GlobalActionExecutor()

    passed = 0
    total = 5

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    result = executor.execute_plan(
        {
            "decision": "select",
            "action": "open",
            "target": None,
        }
    )

    if result.get("success") is False:
        print("[1] Selection Safety PASS")
        passed += 1
    else:
        print("[1] Selection Safety FAIL")

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    result = executor.execute_plan(
        {
            "decision": "reject",
            "action": "open",
            "target": None,
        }
    )

    if result.get("success") is False:
        print("[2] Reject Safety PASS")
        passed += 1
    else:
        print("[2] Reject Safety FAIL")

    # --------------------------------------------------------
    # TEST 3
    # --------------------------------------------------------

    class FakeTarget:
        name = "Test"
        item_type = "file"
        location = None
        target = None
        executable = None
        launchable = False
        capabilities = ["open"]

    normalized = executor.target_to_dict(
        FakeTarget()
    )

    if (
        isinstance(normalized, dict)
        and normalized.get("name") == "Test"
    ):
        print("[3] DiscoveryRecord Adapter PASS")
        passed += 1
    else:
        print("[3] DiscoveryRecord Adapter FAIL")

    # --------------------------------------------------------
    # TEST 4
    # --------------------------------------------------------

    result = executor.execute_target(
        {
            "name": "Test",
            "item_type": "file",
            "location": "C:\\does-not-exist-test",
        }
    )

    if isinstance(result, dict):
        print("[4] Target Normalization PASS")
        passed += 1
    else:
        print("[4] Target Normalization FAIL")

    # --------------------------------------------------------
    # TEST 5
    # --------------------------------------------------------

    result = executor.execute_plan(
        {
            "decision": "execute",
            "action": "open",
            "target": {
                "name": "Test",
                "item_type": "unknown",
            },
        }
    )

    if (
        isinstance(result, dict)
        and result.get("success") is False
    ):
        print("[5] Safe Execution Failure PASS")
        passed += 1
    else:
        print("[5] Safe Execution Failure FAIL")

    print()
    print("=" * 64)
    print(f"Tests passed : {passed}/{total}")

    if passed == total:
        print("GLOBAL ACTION EXECUTOR TEST: PASS")
    else:
        print("GLOBAL ACTION EXECUTOR TEST: FAIL")

    print("=" * 64)
    print()

    return passed == total


if __name__ == "__main__":
    raise SystemExit(
        0 if run_tests() else 1
    )
