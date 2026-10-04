# -*- coding: utf-8 -*-

"""
============================================================
MYX - Global Search Action Integration
============================================================

STEP 11.12

Architecture:

    RealGlobalSearch
            ↓
    GlobalSearchIntelligence
            ↓
    GlobalSearchActionIntegration
            ↓
    GlobalCommandPlanner
            ↓
    Global Action Pipeline

Responsibilities:
    - Create the real search engine.
    - Connect it to GlobalSearchIntelligence.
    - Parse action + target from a natural-language command.
    - Search for action targets.
    - Return an action-ready plan.
    - Provide result helpers.
    - NEVER execute actions.

Execution belongs to:
    GlobalActionExecutor

Selection belongs to:
    GlobalSelectionManager

Safety belongs to:
    GlobalActionSafetyManager
============================================================
"""

import os
import sys


# ============================================================
# PROJECT BOOTSTRAP
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SRC_DIR = os.path.dirname(
    os.path.dirname(CURRENT_DIR)
)

PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# SEARCH COMPONENTS
# ============================================================

from src.system.real_global_search import RealGlobalSearch

from src.system.search.global_search_intelligence import (
    GlobalSearchIntelligence,
)


# ============================================================
# GLOBAL SEARCH ACTION INTEGRATION
# ============================================================

class GlobalSearchActionIntegration:
    """
    Adapter between global search intelligence and
    the action planning layer.

    This class does NOT execute actions.
    """

    # --------------------------------------------------------
    # Supported action words
    # --------------------------------------------------------

    ACTION_ALIASES = {
        "open": "open",
        "launch": "open",
        "start": "open",
        "run": "open",

        "close": "close",
        "exit": "close",
        "quit": "close",

        "delete": "delete",
        "remove": "delete",

        "find": "find",
        "search": "find",
        "locate": "find",

        "show": "show",
        "view": "show",

        "play": "play",

        "stop": "stop",

        "pause": "pause",
    }

    # --------------------------------------------------------
    # Initialization
    # --------------------------------------------------------

    def __init__(
        self,
        search_intelligence=None,
        search_engine=None,
    ):
        """
        Initialize the search/action integration layer.

        A real search engine is created automatically unless
        a test double or custom engine is supplied.
        """

        # ----------------------------------------------------
        # Search engine
        # ----------------------------------------------------

        if search_engine is None:
            search_engine = RealGlobalSearch()

        self.search_engine = search_engine

        # ----------------------------------------------------
        # Search intelligence
        # ----------------------------------------------------

        if search_intelligence is None:
            self.search_intelligence = (
                GlobalSearchIntelligence(
                    search_engine=self.search_engine
                )
            )
        else:
            self.search_intelligence = search_intelligence

            if getattr(
                self.search_intelligence,
                "search_engine",
                None,
            ) is None:
                self.search_intelligence.search_engine = (
                    self.search_engine
                )

        print(
            "[GlobalSearchActionIntegration] "
            "Initialized"
        )

    # ========================================================
    # COMMAND NORMALIZATION
    # ========================================================

    def normalize_command(self, command):
        """
        Normalize an incoming command.
        """

        return str(command or "").strip()

    # ========================================================
    # ACTION RESOLUTION
    # ========================================================

    def resolve_action(self, command):
        """
        Resolve the first meaningful command word
        into a canonical action.

        Example:

            Open Chrome
                ↓
            open

        Returns:
            str | None
        """

        command = self.normalize_command(command)

        if not command:
            return None

        words = command.lower().split()

        if not words:
            return None

        first_word = words[0]

        return self.ACTION_ALIASES.get(
            first_word
        )

    # ========================================================
    # QUERY RESOLUTION
    # ========================================================

    def resolve_query(self, command):
        """
        Remove the action word from the command.

        Example:

            Open Chrome
                ↓
            Chrome

        Example:

            Launch Google Chrome
                ↓
            Google Chrome
        """

        command = self.normalize_command(command)

        if not command:
            return ""

        words = command.split(
            maxsplit=1
        )

        if len(words) == 1:
            return ""

        action = words[0].lower()

        if action in self.ACTION_ALIASES:
            return words[1].strip()

        return command

    # ========================================================
    # SEARCH
    # ========================================================

    def search_targets(self, query):
        """
        Search for action targets.

        Returns:
            list
        """

        query = str(query or "").strip()

        if not query:
            return []

        try:
            results = self.search_intelligence.search(
                query
            )

            if results is None:
                return []

            if isinstance(results, list):
                return results

            if isinstance(results, tuple):
                return list(results)

            return []

        except Exception as e:
            print(
                "[GlobalSearchActionIntegration] "
                f"Search error: {e}"
            )

            return []

    # ========================================================
    # COMPATIBILITY ALIAS
    # ========================================================

    search = search_targets

    # ========================================================
    # BUILD ACTION PLAN
    # ========================================================

    def build_action_plan(self, command):
        """
        Convert a natural-language command into an
        action-ready plan.

        IMPORTANT:
            This method DOES NOT execute anything.

        Example:

            Open Chrome

        becomes:

            {
                "success": True,
                "command": "Open Chrome",
                "action": "open",
                "query": "Chrome",
                "results": [...],
                "result_count": 2
            }
        """

        command = self.normalize_command(command)

        # ----------------------------------------------------
        # Empty command
        # ----------------------------------------------------

        if not command:
            return {
                "success": False,
                "command": "",
                "action": None,
                "query": "",
                "results": [],
                "result_count": 0,
                "reason": "Empty command",
            }

        # ----------------------------------------------------
        # Resolve action
        # ----------------------------------------------------

        action = self.resolve_action(
            command
        )

        # ----------------------------------------------------
        # Unknown action
        # ----------------------------------------------------

        if action is None:
            return {
                "success": False,
                "command": command,
                "action": None,
                "query": command,
                "results": [],
                "result_count": 0,
                "reason": "Unknown action",
            }

        # ----------------------------------------------------
        # Resolve target query
        # ----------------------------------------------------

        query = self.resolve_query(
            command
        )

        # ----------------------------------------------------
        # Action without target
        # ----------------------------------------------------

        if not query:
            return {
                "success": False,
                "command": command,
                "action": action,
                "query": "",
                "results": [],
                "result_count": 0,
                "reason": "No target specified",
            }

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        results = self.search_targets(
            query
        )

        # ----------------------------------------------------
        # Return plan
        # ----------------------------------------------------

        return {
            "success": bool(results),
            "command": command,
            "action": action,
            "query": query,
            "results": results,
            "result_count": len(results),
            "reason": (
                "Matching results found"
                if results
                else "No matching results"
            ),
        }

    # ========================================================
    # RESULT COUNT
    # ========================================================

    def result_count(self, query):
        """
        Return number of matching results.
        """

        return len(
            self.search_targets(query)
        )

    # ========================================================
    # TOP RESULT
    # ========================================================

    def top_result(self, query):
        """
        Return the first matching result.

        Returns:
            DiscoveryRecord | dict | None
        """

        results = self.search_targets(
            query
        )

        if not results:
            return None

        return results[0]

    # ========================================================
    # RESULT DESCRIPTION
    # ========================================================

    def describe_result(self, record):
        """
        Convert a search record into a simple
        information dictionary.

        Supports DiscoveryRecord and compatible
        search result objects.
        """

        if record is None:
            return {
                "name": "",
                "item_type": "",
                "path": "",
            }

        try:
            name = self.search_intelligence.get_name(
                record
            )

            item_type = (
                self.search_intelligence.get_item_type(
                    record
                )
            )

            path = self.search_intelligence.get_path(
                record
            )

            return {
                "name": str(name or ""),
                "item_type": str(
                    item_type or ""
                ),
                "path": str(path or ""),
            }

        except Exception as e:
            print(
                "[GlobalSearchActionIntegration] "
                f"Result description error: {e}"
            )

            return {
                "name": "",
                "item_type": "",
                "path": "",
            }


# ============================================================
# TEST SUITE
# ============================================================

def run_test():
    """
    Integration-layer isolation test.

    This test verifies:
        1. Initialization
        2. Empty command handling
        3. Action parsing
        4. Query parsing
        5. Action plan generation
        6. Result helpers
    """

    print()
    print("=" * 60)
    print(
        "       MYX GLOBAL SEARCH ACTION INTEGRATION TEST"
    )
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Initialization
    # --------------------------------------------------------

    try:
        integration = (
            GlobalSearchActionIntegration()
        )

        print(
            "[1] Initialization : PASS"
        )

    except Exception as e:
        print(
            "[1] Initialization : FAIL"
        )
        print("    Error:", e)

        return False

    # --------------------------------------------------------
    # 2. Empty command
    # --------------------------------------------------------

    try:
        result = (
            integration.build_action_plan("")
        )

        if (
            result.get("success") is False
            and result.get("action") is None
        ):
            print(
                "[2] Empty command : PASS"
            )
        else:
            print(
                "[2] Empty command : FAIL"
            )
            print(
                "    Result:",
                result
            )

            return False

    except Exception as e:
        print(
            "[2] Empty command : FAIL"
        )
        print("    Error:", e)

        return False

    # --------------------------------------------------------
    # 3. Action resolution
    # --------------------------------------------------------

    try:
        action = integration.resolve_action(
            "Open Chrome"
        )

        if action == "open":
            print(
                "[3] Action resolution : PASS"
            )
        else:
            print(
                "[3] Action resolution : FAIL"
            )
            print(
                "    Action:",
                action
            )

            return False

    except Exception as e:
        print(
            "[3] Action resolution : FAIL"
        )
        print("    Error:", e)

        return False

    # --------------------------------------------------------
    # 4. Query resolution
    # --------------------------------------------------------

    try:
        query = integration.resolve_query(
            "Open Chrome"
        )

        if query.lower() == "chrome":
            print(
                "[4] Query resolution : PASS"
            )
        else:
            print(
                "[4] Query resolution : FAIL"
            )
            print(
                "    Query:",
                query
            )

            return False

    except Exception as e:
        print(
            "[4] Query resolution : FAIL"
        )
        print("    Error:", e)

        return False

    # --------------------------------------------------------
    # 5. Build action plan
    # --------------------------------------------------------

    try:
        plan = integration.build_action_plan(
            "Open Chrome"
        )

        print(
            "[5] Action plan generation : PASS"
        )

        print()
        print(
            "    Action:",
            plan.get("action")
        )

        print(
            "    Query:",
            plan.get("query")
        )

        print(
            "    Result Count:",
            plan.get("result_count")
        )

        print(
            "    Reason:",
            plan.get("reason")
        )

    except Exception as e:
        print(
            "[5] Action plan generation : FAIL"
        )
        print("    Error:", e)

        return False

    # --------------------------------------------------------
    # 6. Result helper
    # --------------------------------------------------------

    try:
        count = integration.result_count(
            "Chrome"
        )

        print(
            "[6] Result helper : PASS"
        )

        print(
            "    Chrome results:",
            count
        )

    except Exception as e:
        print(
            "[6] Result helper : FAIL"
        )
        print("    Error:", e)

        return False

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print(
        "MYX GLOBAL SEARCH ACTION INTEGRATION TEST : PASS"
    )
    print("=" * 60)

    return True


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":
    success = run_test()

    raise SystemExit(
        0 if success else 1
    )
