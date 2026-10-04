# -*- coding: utf-8 -*-

"""
============================================================
MYX / MAYAX AI
MEMORY CONTEXT
============================================================

Purpose:
    Provide clean, relevant persistent memory context
    to the Brain.

Architecture:

    MemoryManager
         ↓
    MemoryRelevance
         ↓
    MemoryContext
         ↓
       Brain

Responsibilities:
    - connect to MemoryManager
    - retrieve persistent memories
    - use MemoryRelevance for ranking
    - build clean context
    - format context for Brain
    - expose health status

Does NOT:
    - modify database directly
    - execute actions
    - call external AI
============================================================
"""

from typing import Any, Dict, List


class MemoryContext:

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        memory_manager=None,
        relevance_engine=None
    ):

        self.memory_manager = memory_manager

        # ----------------------------------------------------
        # Relevance Engine
        # ----------------------------------------------------

        if relevance_engine is not None:

            self.relevance = relevance_engine

        else:

            try:

                from src.memory.memory_relevance import (
                    MemoryRelevance
                )

                self.relevance = MemoryRelevance(
                    memory_manager=self.memory_manager
                )

            except Exception as e:

                self.relevance = None

                print(
                    "[MemoryContext] Relevance "
                    f"import warning: {e}"
                )

        print(
            "[MemoryContext] Initialized"
        )

    # ========================================================
    # CONNECTION
    # ========================================================

    def connected(self) -> bool:
        """
        Check MemoryManager connection.
        """

        return (
            self.memory_manager is not None
        )

    # ========================================================
    # RELEVANCE CONNECTION
    # ========================================================

    def relevance_connected(self) -> bool:
        """
        Check MemoryRelevance connection.
        """

        return (
            self.relevance is not None
        )

    # ========================================================
    # RECALL ONE
    # ========================================================

    def recall(
        self,
        key,
        default=None
    ):
        """
        Recall a specific memory.
        """

        if not self.connected():

            return default

        try:

            return self.memory_manager.recall(
                key,
                default
            )

        except Exception as e:

            print(
                "[MemoryContext] Recall warning: "
                f"{e}"
            )

            return default

    # ========================================================
    # RECALL ALL
    # ========================================================

    def recall_all(self) -> List[Any]:
        """
        Return all persistent memories.
        """

        if not self.connected():

            return []

        try:

            memories = (
                self.memory_manager.recall_all()
            )

            if memories is None:

                return []

            return list(memories)

        except Exception as e:

            print(
                "[MemoryContext] Recall all warning: "
                f"{e}"
            )

            return []

    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    def build_context(
        self,
        user_input=None,
        limit=10,
        min_score=1.0
    ) -> Dict[str, Any]:
        """
        Build relevant memory context.

        If user_input is available, memories are ranked
        through MemoryRelevance.

        If no query is supplied, return an empty relevant
        context rather than dumping all memories.
        """

        query = (
            str(user_input).strip()
            if user_input is not None
            else ""
        )

        # ----------------------------------------------------
        # Base Context
        # ----------------------------------------------------

        context = {
            "available": self.connected(),
            "relevance_available": (
                self.relevance_connected()
            ),
            "query": query,
            "memories": [],
            "count": 0,
        }

        if not self.connected():

            return context

        # ----------------------------------------------------
        # No query
        # ----------------------------------------------------

        if not query:

            return context

        # ----------------------------------------------------
        # Relevance Engine
        # ----------------------------------------------------

        if self.relevance is not None:

            try:

                results = (
                    self.relevance.find_relevant(
                        query=query,
                        limit=limit,
                        min_score=min_score
                    )
                )

                if results is None:

                    results = []

                context["memories"] = list(
                    results
                )

                context["count"] = len(
                    context["memories"]
                )

                return context

            except Exception as e:

                print(
                    "[MemoryContext] Relevance "
                    f"warning: {e}"
                )

        # ----------------------------------------------------
        # Safe fallback
        # ----------------------------------------------------

        return context

    # ========================================================
    # FORMAT CONTEXT
    # ========================================================

    def format_context(
        self,
        context: Dict[str, Any]
    ) -> str:
        """
        Convert relevant memory context into readable text.
        """

        if not isinstance(
            context,
            dict
        ):

            return ""

        memories = context.get(
            "memories",
            []
        )

        if not memories:

            return ""

        lines = []

        for item in memories:

            # ------------------------------------------------
            # Relevance result
            # ------------------------------------------------

            if isinstance(
                item,
                dict
            ):

                key = item.get(
                    "key",
                    ""
                )

                value = item.get(
                    "value",
                    ""
                )

                if key:

                    lines.append(
                        f"{key}: {value}"
                    )

                continue

            # ------------------------------------------------
            # SQLite Row
            # ------------------------------------------------

            if hasattr(
                item,
                "keys"
            ):

                try:

                    keys = item.keys()

                    if (
                        "key" in keys
                        and "value" in keys
                    ):

                        lines.append(
                            f"{item['key']}: "
                            f"{item['value']}"
                        )

                except Exception:

                    continue

                continue

            # ------------------------------------------------
            # Tuple / List
            # ------------------------------------------------

            if isinstance(
                item,
                (tuple, list)
            ):

                if len(item) >= 3:

                    lines.append(
                        f"{item[1]}: {item[2]}"
                    )

                elif len(item) == 2:

                    lines.append(
                        f"{item[0]}: {item[1]}"
                    )

        return "\n".join(
            lines
        )

    # ========================================================
    # RELEVANT TEXT
    # ========================================================

    def get_relevant_text(
        self,
        user_input=None,
        limit=5,
        min_score=1.0
    ) -> str:
        """
        Convenience API for Brain.
        """

        context = self.build_context(
            user_input=user_input,
            limit=limit,
            min_score=min_score
        )

        return self.format_context(
            context
        )

    # ========================================================
    # HEALTH
    # ========================================================

    def health(self) -> Dict[str, bool]:
        """
        Return MemoryContext subsystem health.
        """

        return {
            "memory_context": True,
            "memory_manager_connected": (
                self.connected()
            ),
            "memory_relevance_connected": (
                self.relevance_connected()
            ),
        }


# ============================================================
# STANDALONE TEST
# ============================================================

def run_memory_context_test():

    print()
    print("=" * 60)
    print(
        "          MYX MEMORY CONTEXT TEST"
    )
    print("=" * 60)

    class FakeMemoryManager:

        def __init__(self):

            self.memories = [
                (
                    1,
                    "name",
                    "Avishkar"
                ),
                (
                    2,
                    "project",
                    "MyX AI Assistant"
                ),
                (
                    3,
                    "language",
                    "Marathi"
                ),
                (
                    4,
                    "editor",
                    "Cursor"
                ),
            ]

        def recall(
            self,
            key,
            default=None
        ):

            for item in self.memories:

                if item[1] == key:

                    return item[2]

            return default

        def recall_all(self):

            return self.memories

    try:

        # ----------------------------------------------------
        # Create fake memory manager
        # ----------------------------------------------------

        manager = FakeMemoryManager()

        context_engine = MemoryContext(
            memory_manager=manager
        )

        # ----------------------------------------------------
        # Test 1
        # ----------------------------------------------------

        if context_engine.connected():

            print(
                "[1] Memory Connection : PASS"
            )

        else:

            print(
                "[1] Memory Connection : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 2
        # ----------------------------------------------------

        if context_engine.relevance_connected():

            print(
                "[2] Relevance Connection : PASS"
            )

        else:

            print(
                "[2] Relevance Connection : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 3
        # ----------------------------------------------------

        value = context_engine.recall(
            "project"
        )

        if value == "MyX AI Assistant":

            print(
                "[3] Memory Recall : PASS"
            )

        else:

            print(
                "[3] Memory Recall : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 4
        # ----------------------------------------------------

        memories = context_engine.recall_all()

        if len(memories) == 4:

            print(
                "[4] Memory List : PASS"
            )

        else:

            print(
                "[4] Memory List : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 5
        # ----------------------------------------------------

        context = context_engine.build_context(
            user_input="What is my MyX project?",
            limit=3
        )

        if (
            context["count"] >= 1
            and context["relevance_available"] is True
        ):

            print(
                "[5] Relevant Context : PASS"
            )

        else:

            print(
                "[5] Relevant Context : FAIL"
            )

            print(
                "    Context:",
                context
            )

            return False

        # ----------------------------------------------------
        # Test 6
        # ----------------------------------------------------

        formatted = (
            context_engine.format_context(
                context
            )
        )

        if (
            "project:" in formatted
            and "MyX AI Assistant" in formatted
        ):

            print(
                "[6] Context Format : PASS"
            )

        else:

            print(
                "[6] Context Format : FAIL"
            )

            print(
                "    Formatted:",
                formatted
            )

            return False

        # ----------------------------------------------------
        # Test 7
        # ----------------------------------------------------

        relevant_text = (
            context_engine.get_relevant_text(
                "What is my project?"
            )
        )

        if (
            isinstance(
                relevant_text,
                str
            )
            and "project:" in relevant_text
        ):

            print(
                "[7] Relevant Text API : PASS"
            )

        else:

            print(
                "[7] Relevant Text API : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 8
        # ----------------------------------------------------

        health = (
            context_engine.health()
        )

        if (
            health["memory_context"] is True
            and health[
                "memory_manager_connected"
            ] is True
            and health[
                "memory_relevance_connected"
            ] is True
        ):

            print(
                "[8] Health : PASS"
            )

        else:

            print(
                "[8] Health : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Final
        # ----------------------------------------------------

        print("=" * 60)
        print(
            "       MYX MEMORY CONTEXT : PASS"
        )
        print("=" * 60)

        return True

    except Exception as e:

        print(
            "[MemoryContext Test] FAIL:",
            e
        )

        return False


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    success = (
        run_memory_context_test()
    )

    raise SystemExit(
        0 if success else 1
    )
