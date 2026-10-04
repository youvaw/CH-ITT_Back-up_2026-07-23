# -*- coding: utf-8 -*-

"""MYX / MAYAX AI - Global Action Pipeline.

Command -> Search -> Plan -> Safety -> Selection -> Commit -> Execute -> Audit
Discovery-first; no app-specific hardcoding.
"""

from __future__ import annotations

from datetime import datetime
import importlib

from src.tools.tool_router import ToolRouter
from src.system.real_global_search import RealGlobalSearch
from src.system.search.global_search_intelligence import GlobalSearchIntelligence


REJECT_DECISIONS = {"reject", "denied", "blocked", "forbidden"}
SELECT_DECISIONS = {"select", "selection", "choose", "clarify"}
EXECUTE_DECISIONS = {"execute", "run", "open", "launch", "perform"}


def _safe_construct(module_name, class_names):
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:
        print(f"[GlobalActionPipeline] Import warning {module_name}: {exc}")
        return None
    for class_name in class_names:
        cls = getattr(module, class_name, None)
        if cls is None or not callable(cls):
            continue
        try:
            return cls()
        except TypeError:
            continue
        except Exception as exc:
            print(f"[GlobalActionPipeline] Initialization warning {module_name}.{class_name}: {exc}")
    return None


class GlobalActionPipeline:
    """Central orchestration layer for global MYX actions."""

    def __init__(
        self,
        search=None,
        planner=None,
        safety=None,
        selection=None,
        executor=None,
        audit=None,
        tool_router=None,
    ):
        self.search = (
            search
            if search is not None
            else GlobalSearchIntelligence(RealGlobalSearch())
        )
        self.planner = (
            planner
            if planner is not None
            else _safe_construct(
                "src.system.real_global_action_resolver",
                ("RealGlobalActionResolver",),
            )
        )
        self.safety = (
            safety
            if safety is not None
            else _safe_construct(
                "src.system.actions.global_action_safety_manager",
                ("GlobalActionSafetyManager",),
            )
        )
        self.selection = (
            selection
            if selection is not None
            else _safe_construct(
                "src.system.actions.global_selection_manager",
                ("GlobalSelectionManager",),
            )
        )
        self.executor = (
            executor
            if executor is not None
            else _safe_construct(
                "src.system.actions.global_action_executor",
                ("GlobalActionExecutor",),
            )
        )
        self.audit = (
            audit
            if audit is not None
            else _safe_construct(
                "src.system.actions.global_action_audit",
                ("GlobalActionAudit",),
            )
        )
        self.tool_router = (
            tool_router
            if tool_router is not None
            else ToolRouter()
        )
        print("[GlobalActionPipeline] Initialized")

    @staticmethod
    def _call_first(component, method_names, arg_variants):
        if component is None:
            return False, None
        for method_name in method_names:
            method = getattr(component, method_name, None)
            if not callable(method):
                continue
            for args, kwargs in arg_variants:
                try:
                    return True, method(*args, **kwargs)
                except TypeError:
                    continue
                except Exception as exc:
                    print(f"[GlobalActionPipeline] {method_name} error: {exc}")
                    return True, None
        return False, None

    @staticmethod
    def _normalize_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, (tuple, set)):
            return list(value)
        return [value]

    @staticmethod
    def _normalize_action(command):
        text = str(command or "").strip().lower()
        if any(x in text for x in ("open", "launch", "start", "run")):
            return "open"
        if any(x in text for x in ("close", "exit", "quit", "stop")):
            return "close"
        if any(x in text for x in ("find", "locate", "where")):
            return "find"
        if any(x in text for x in ("search", "look for")):
            return "search"
        return "search"

    @staticmethod
    def _extract_query(command):
        text = str(command or "").strip()
        prefixes = (
            "search for ", "where is ", "open ", "launch ", "start ",
            "run ", "close ", "exit ", "quit ", "stop ", "find ",
            "locate ", "search ",
        )
        lowered = text.lower()
        for prefix in prefixes:
            if lowered.startswith(prefix):
                return text[len(prefix):].strip()
        return text

    # ----------------------------- SEARCH -----------------------------
    def search_targets(self, command):
        command = str(command or "").strip()
        if not command or self.search is None:
            return []
        query = self._extract_query(command)
        called, result = self._call_first(
            self.search,
            ("search", "search_records", "find", "query"),
            (((query,), {}), ((command,), {})),
        )
        if not called:
            return []
        if isinstance(result, dict):
            for key in ("results", "candidates", "records", "items"):
                if key in result:
                    return self._normalize_list(result[key])
            return []
        return self._normalize_list(result)

    # ----------------------------- PLAN -----------------------------
    def create_plan(self, command, candidates):
        command = str(command or "").strip()
        candidates = self._normalize_list(candidates)

        fallback = {
            "command": command,
            "action": self._normalize_action(command),
            "query": self._extract_query(command),
            "decision": "select" if len(candidates) > 1 else "execute",
            "target": candidates[0] if len(candidates) == 1 else None,
            "candidates": candidates,
            "results": candidates,
            "result_count": len(candidates),
            "requires_selection": len(candidates) > 1,
            "requires_confirmation": False,
        }

        if self.planner is None:
            return fallback

        called, result = self._call_first(
            self.planner,
            ("plan", "create_plan", "resolve", "process", "run"),
            (
                ((command, candidates), {}),
                ((command,), {}),
            ),
        )

        if not called or not isinstance(result, dict):
            return fallback

        plan = dict(fallback)
        plan.update(result)

        # Resolver-selected target has highest priority.
        # RealGlobalActionResolver may return `selected`,
        # while the execution pipeline expects `target`.
        selected = plan.get("selected")
        if selected is not None:
            plan["target"] = selected

        resolved_results = (
            plan.get("results")
            or plan.get("candidates")
            or plan.get("items")
            or candidates
        )
        resolved_results = self._normalize_list(resolved_results)

        plan["results"] = resolved_results
        plan["candidates"] = (
            self._normalize_list(plan.get("candidates"))
            or resolved_results
        )
        plan["result_count"] = len(resolved_results)
        plan["action"] = plan.get("action") or fallback["action"]
        plan["query"] = plan.get("query") or fallback["query"]

        decision = str(plan.get("decision", "")).strip().lower()

        if decision in REJECT_DECISIONS:
            plan["decision"] = "reject"
        elif decision in EXECUTE_DECISIONS:
            plan["decision"] = "execute"
        elif plan.get("target") is not None:
            plan["decision"] = "execute"
        elif len(resolved_results) == 1:
            plan["decision"] = "execute"
        elif decision in SELECT_DECISIONS or not decision:
            plan["decision"] = "select"
        else:
            plan["decision"] = "select"

        if plan.get("target") is not None:
            plan["decision"] = "execute"
            plan["requires_selection"] = False
        else:
            plan["requires_selection"] = plan["decision"] == "select"

        plan.setdefault("requires_confirmation", False)
        return plan

    # ----------------------------- SAFETY -----------------------------
    def check_safety(self, plan):
        if self.safety is None:
            decision = str(plan.get("decision", "execute")).lower()
            return {
                "decision": "reject" if decision in REJECT_DECISIONS else "execute",
                "allowed": decision not in REJECT_DECISIONS,
                "reason": "No safety manager configured.",
            }
        called, result = self._call_first(
            self.safety,
            ("evaluate", "check", "decide", "validate"),
            (((plan,), {}),),
        )
        if called and result is not None:
            if isinstance(result, dict):
                out = dict(result)
                if "allowed" not in out:
                    out["allowed"] = str(out.get("decision", "")).lower() not in REJECT_DECISIONS
                return out
            if isinstance(result, bool):
                return {"decision": "execute" if result else "reject", "allowed": result}
            decision = str(result).lower()
            return {"decision": decision, "allowed": decision not in REJECT_DECISIONS}
        decision = str(plan.get("decision", "execute")).lower()
        return {"decision": "reject" if decision in REJECT_DECISIONS else "execute",
                "allowed": decision not in REJECT_DECISIONS}

    # ----------------------------- SELECTION -----------------------------
    def select_target(self, candidates, plan):
        candidates = self._normalize_list(candidates)
        if not candidates:
            candidates = self._normalize_list(plan.get("results", []))
        if not candidates:
            return plan.get("target")

        if self.selection is not None:
            for name in ("set_candidates", "set_results", "load", "update"):
                method = getattr(self.selection, name, None)
                if callable(method):
                    try:
                        method(candidates)
                        break
                    except TypeError:
                        continue
                    except Exception as exc:
                        print(f"[GlobalActionPipeline] Selection storage error: {exc}")
                        break

        requested = plan.get("target")
        if requested is not None:
            if self.selection is not None:
                for name in ("select", "select_candidate", "choose", "resolve_selection"):
                    method = getattr(self.selection, name, None)
                    if not callable(method):
                        continue
                    for args in ((requested,), (candidates, requested)):
                        try:
                            selected = method(*args)
                            if selected is not None:
                                return selected
                        except TypeError:
                            continue
                        except Exception as exc:
                            print(f"[GlobalActionPipeline] Explicit selection error: {exc}")
                            break
            return requested

        return candidates[0] if len(candidates) == 1 else None

    # ============================================================
    # LOCAL TOOL ROUTING
    # ============================================================

    def match_local_tool(self, command):
        """Match a deterministic local tool request without executing it."""
        if self.tool_router is None:
            return None
        try:
            return self.tool_router.match(command)
        except Exception as exc:
            print(
                "[GlobalActionPipeline] "
                f"Local tool match warning: {exc}"
            )
            return None

    def create_local_tool_plan(self, command, tool_request):
        """Convert a ToolRouter request into the standard pipeline plan."""
        if not isinstance(tool_request, dict):
            return {
                "command": command,
                "action": "local_tool",
                "query": command,
                "decision": "reject",
                "target": None,
                "candidates": [],
                "results": [],
                "result_count": 0,
                "requires_selection": False,
                "requires_confirmation": False,
            }

        return {
            "command": command,
            "action": "local_tool",
            "query": command,
            "decision": "execute",
            "target": tool_request,
            "candidates": [tool_request],
            "results": [tool_request],
            "result_count": 1,
            "requires_selection": False,
            "requires_confirmation": False,
            "tool": tool_request.get("tool"),
            "tool_action": tool_request.get("action"),
        }

    def _commit_selection(self, plan, target):
        execution_plan = dict(plan)
        execution_plan["target"] = target
        execution_plan["decision"] = "execute"
        execution_plan["requires_selection"] = False
        execution_plan.setdefault("requires_confirmation", False)
        return execution_plan

    # ----------------------------- EXECUTION -----------------------------
    def execute_action(self, plan, target):
        # Local deterministic tools are executed through ToolRouter.
        if isinstance(target, dict) and target.get("tool"):
            if self.tool_router is None:
                return {
                    "success": False,
                    "stage": "execution",
                    "message": "Local Tool Router is unavailable.",
                }

            try:
                result = self.tool_router.execute(target)
                if isinstance(result, dict):
                    result.setdefault("stage", "execution")
                return result
            except Exception as exc:
                return {
                    "success": False,
                    "stage": "execution",
                    "tool": target.get("tool"),
                    "action": target.get("action"),
                    "message": str(exc),
                }

        # Existing global executor path.
        if self.executor is None:
            return {"success": False, "message": "Global Action Executor is unavailable."}
        if target is None:
            return {"success": False, "message": "A concrete target is required before execution."}
        execution_plan = self._commit_selection(plan, target)
        for name in ("execute_plan", "execute", "run", "perform"):
            method = getattr(self.executor, name, None)
            if not callable(method):
                continue
            attempts = (
                ((execution_plan,), {}),
                ((execution_plan.get("action"), target), {}),
                ((target,), {}),
            )
            for args, kwargs in attempts:
                try:
                    result = method(*args, **kwargs)
                    if isinstance(result, dict):
                        return result
                    if isinstance(result, bool):
                        return {
                            "success": result,
                            "message": "Action executed successfully." if result else "Action execution failed.",
                        }
                    return {"success": True, "message": str(result)}
                except TypeError:
                    continue
                except Exception as exc:
                    return {"success": False, "message": str(exc)}
        return {"success": False, "message": "No compatible executor method found."}

    # ----------------------------- AUDIT -----------------------------
    def audit_action(self, command, plan, target, result, safety=None):
        if self.audit is None:
            return None
        success = bool(result.get("success", False)) if isinstance(result, dict) else False
        message = str(result.get("message", "")) if isinstance(result, dict) else str(result)
        record = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "action": plan.get("action", "unknown"),
            "decision": safety.get("decision", "unknown") if isinstance(safety, dict) else "unknown",
            "target": target,
            "success": success,
            "message": message,
        }
        method = getattr(self.audit, "add_record", None)
        if callable(method):
            try:
                method(record)
                return record
            except Exception:
                pass
        method = getattr(self.audit, "record_result", None)
        if callable(method):
            try:
                method(command=command, action=record["action"], decision=record["decision"],
                       target=target, success=success, message=message)
            except Exception:
                pass
        return record

    # ----------------------------- MAIN -----------------------------
    def process(self, command):
        command = str(command or "").strip()
        if not command:
            return {"success": False, "stage": "input", "message": "Command is empty."}

        # Local deterministic tools are checked before discovery/search.
        local_tool = self.match_local_tool(command)

        if local_tool is not None:
            candidates = [local_tool]
            plan = self.create_local_tool_plan(command, local_tool)
        else:
            candidates = self.search_targets(command)
            plan = self.create_plan(command, candidates)
            if not isinstance(plan, dict):
                plan = {
                    "command": command,
                    "action": self._normalize_action(command),
                    "query": self._extract_query(command),
                    "decision": "select",
                    "target": None,
                    "candidates": candidates,
                    "results": candidates,
                }

        safety = self.check_safety(plan)
        if not isinstance(safety, dict):
            safety = {"decision": "execute", "allowed": True}
        if not bool(safety.get("allowed", True)) or str(safety.get("decision", "")).lower() in REJECT_DECISIONS:
            result = {"success": False, "stage": "safety",
                      "message": safety.get("reason", "Action rejected by safety manager."),
                      "plan": plan}
            self.audit_action(command, plan, None, result, safety)
            return result

        target = self.select_target(candidates, plan)
        effective = self._normalize_list(candidates) or self._normalize_list(plan.get("results", []))
        if target is None:
            result = {
                "success": False,
                "stage": "selection",
                "decision": "select",
                "message": ("Multiple targets found. Selection is required before execution."
                            if len(effective) > 1 else "No matching target found."),
                "candidates": effective,
                "plan": plan,
            }
            self.audit_action(command, plan, None, result, safety)
            return result

        execution_plan = self._commit_selection(plan, target)
        result = self.execute_action(execution_plan, target)
        if not isinstance(result, dict):
            result = {"success": True, "message": str(result)}
        self.audit_action(command, execution_plan, target, result, safety)
        result.setdefault("stage", "execution")
        result.setdefault("target", target)
        result.setdefault("plan", execution_plan)
        result.setdefault("decision", "execute")
        return result

    run = process


# =============================================================
# STANDALONE TESTS
# =============================================================
class _FakeSearch:
    def search(self, command):
        return [{"name": "Test Application", "item_type": "application"}]


class _FakePlanner:
    def plan(self, command, candidates):
        return {"command": command, "action": "open", "decision": "execute",
                "target": candidates[0], "candidates": candidates, "results": candidates}


class _FakeSafety:
    def evaluate(self, plan):
        return {"decision": "execute", "allowed": True}


class _FakeSelection:
    def __init__(self):
        self.candidates = []
    def set_candidates(self, candidates):
        self.candidates = candidates
    def select(self, target):
        return target


class _FakeExecutor:
    def execute(self, plan):
        return {"success": plan.get("decision") == "execute" and not plan.get("requires_selection", False),
                "message": "TEST EXECUTION SUCCESS"}


class _FakeAudit:
    def __init__(self):
        self.records = []
    def add_record(self, record):
        self.records.append(record)


def run_tests():
    print("\n" + "=" * 70)
    print("MYX GLOBAL ACTION PIPELINE TEST")
    print("PRODUCTION CLEAN VERSION")
    print("=" * 70)
    passed = 0
    total = 13
    p = GlobalActionPipeline(_FakeSearch(), _FakePlanner(), _FakeSafety(), _FakeSelection(), _FakeExecutor(), _FakeAudit())
    checks = []
    candidates = p.search_targets("open test application")
    checks.append(("Initialization", p.search is not None))
    checks.append(("Search stage", len(candidates) == 1))
    plan = p.create_plan("open test application", candidates)
    checks.append(("Planner stage", plan.get("action") == "open"))
    safety = p.check_safety(plan)
    checks.append(("Safety stage", safety.get("allowed") is True))
    target = p.select_target(candidates, plan)
    checks.append(("Selection stage", target == candidates[0]))
    committed = p._commit_selection(plan, target)
    checks.append(("Selection -> Execution Handoff", committed.get("decision") == "execute" and committed.get("requires_selection") is False))
    execution = p.execute_action(committed, target)
    checks.append(("Execution stage", execution.get("success") is True))
    p.audit_action("open test application", committed, target, execution, safety)
    checks.append(("Audit stage", len(p.audit.records) >= 1))
    full = p.process("open test application")
    checks.append(("Full pipeline", full.get("success") is True and full.get("stage") == "execution"))

    class AmbiguousSearch:
        def search(self, command):
            return [{"name": "Google Chrome", "item_type": "application"}, {"name": "ChromeSetup.exe", "item_type": "file"}]
    class AmbiguousPlanner:
        def plan(self, command, candidates):
            return {"action": "open", "decision": "select", "target": None, "results": candidates, "candidates": candidates}
    ambiguous = GlobalActionPipeline(AmbiguousSearch(), AmbiguousPlanner(), _FakeSafety(), _FakeSelection(), _FakeExecutor(), _FakeAudit())
    ar = ambiguous.process("open chrome")
    checks.append(("Ambiguous Target Safety", ar.get("stage") == "selection" and ar.get("success") is False))

    class SelectedPlanner:
        def resolve(self, command):
            selected = {"name": "Google Chrome", "item_type": "application"}
            return {"action": "open", "query": "chrome", "results": [selected, {"name": "ChromeSetup.exe", "item_type": "file"}],
                    "selected": selected, "needs_selection": False}
    selected = GlobalActionPipeline(_FakeSearch(), SelectedPlanner(), _FakeSafety(), _FakeSelection(), _FakeExecutor(), _FakeAudit())
    sp = selected.create_plan("open chrome", selected.search_targets("open chrome"))
    checks.append(("Resolver Selected Target Handoff", sp.get("target", {}).get("name") == "Google Chrome" and sp.get("decision") == "execute"))
    checks.append(("Empty Command Safety", p.process("").get("stage") == "input"))

    local = GlobalActionPipeline(
        _FakeSearch(),
        _FakePlanner(),
        _FakeSafety(),
        _FakeSelection(),
        _FakeExecutor(),
        _FakeAudit(),
    )
    local_request = local.match_local_tool("cpu usage")
    local_result = local.process("cpu usage")
    checks.append((
        "Local Tool Routing",
        isinstance(local_request, dict)
        and local_request.get("tool") == "system"
        and local_result.get("success") is True
        and local_result.get("tool") == "system"
        and local_result.get("action") == "cpu",
    ))

    for i, (name, ok) in enumerate(checks, 1):
        print(f"[{i}] {name} {'PASS' if ok else 'FAIL'}")
        passed += int(ok)
    print("\n" + "=" * 70)
    print(f"Tests passed : {passed}/{total}")
    print("=" * 70)
    print("GLOBAL ACTION PIPELINE TEST: PASS" if passed == total else "GLOBAL ACTION PIPELINE TEST: FAIL")
    print("PRODUCTION CLEAN VERSION: READY" if passed == total else "DO NOT CONNECT TO LAUNCH YET")
    print("=" * 70 + "\n")
    return passed == total


if __name__ == "__main__":
    raise SystemExit(0 if run_tests() else 1)

