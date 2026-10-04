# -*- coding: utf-8 -*-

"""
============================================================
MYX / MAYAX AI
MEMORY RELEVANCE ENGINE
============================================================

Purpose:
    Select memories that are relevant to the current user input.

Architecture:

    User Input
        ↓
    Memory Relevance Engine
        ↓
    Relevant Memories
        ↓
    Memory Context
        ↓
    Brain

Design goals:
    - lightweight
    - deterministic
    - offline
    - no external AI/API
    - safe
    - explainable
    - easy to replace with a stronger semantic engine later

This module does NOT:
    - modify the database
    - modify MemoryManager
    - modify Brain
    - call Gemini
    - execute system actions
============================================================
"""

import re
from typing import Any, Dict, List


class MemoryRelevance:
    """
    Lightweight relevance engine for persistent memories.
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self, memory_manager=None):

        self.memory_manager = memory_manager

        print(
            "[MemoryRelevance] Initialized"
        )

    # ========================================================
    # CONNECTION
    # ========================================================

    def connected(self) -> bool:
        """
        Check whether MemoryManager is available.
        """

        return (
            self.memory_manager is not None
        )

    # ========================================================
    # TEXT NORMALIZATION
    # ========================================================

    @staticmethod
    def normalize(text: Any) -> str:
        """
        Normalize text for comparison.
        """

        if text is None:
            return ""

        text = str(text).lower()

        text = re.sub(
            r"[^a-z0-9\u0900-\u097f\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ========================================================
    # TOKENIZATION
    # ========================================================

    @classmethod
    def tokenize(cls, text: Any) -> List[str]:
        """
        Convert text into unique searchable tokens.
        """

        normalized = cls.normalize(text)

        if not normalized:
            return []

        tokens = normalized.split()

        # Remove extremely short tokens because they usually
        # produce noisy matches.

        tokens = [
            token
            for token in tokens
            if len(token) >= 2
        ]

        return list(
            dict.fromkeys(tokens)
        )

    # ========================================================
    # MEMORY EXTRACTION
    # ========================================================

    @staticmethod
    def extract_memory(item: Any):
        """
        Convert SQLite Row / tuple / dict into:

            key, value
        """

        if item is None:
            return None

        # Dictionary / SQLite Row

        if hasattr(item, "keys"):

            try:

                keys = item.keys()

                if (
                    "key" in keys
                    and "value" in keys
                ):

                    return (
                        str(item["key"]),
                        str(item["value"])
                    )

            except Exception:
                pass

        # Tuple / List

        if isinstance(
            item,
            (tuple, list)
        ):

            if len(item) >= 3:

                return (
                    str(item[1]),
                    str(item[2])
                )

            if len(item) == 2:

                return (
                    str(item[0]),
                    str(item[1])
                )

        return None

    # ========================================================
    # SCORE MEMORY
    # ========================================================

    def score_memory(
        self,
        query: Any,
        memory_key: Any,
        memory_value: Any
    ) -> float:
        """
        Calculate a deterministic relevance score.

        Score components:

            key exact match      = high
            key token match      = strong
            value token match    = normal
            phrase match         = bonus
        """

        query_text = self.normalize(
            query
        )

        key_text = self.normalize(
            memory_key
        )

        value_text = self.normalize(
            memory_value
        )

        if not query_text:

            return 0.0

        if not key_text and not value_text:

            return 0.0

        score = 0.0

        # ----------------------------------------------------
        # Exact phrase match
        # ----------------------------------------------------

        if (
            key_text
            and key_text in query_text
        ):

            score += 10.0

        if (
            value_text
            and value_text in query_text
        ):

            score += 8.0

        # ----------------------------------------------------
        # Reverse phrase match
        # ----------------------------------------------------

        if (
            query_text in key_text
        ):

            score += 7.0

        if (
            query_text in value_text
        ):

            score += 6.0

        # ----------------------------------------------------
        # Token matching
        # ----------------------------------------------------

        query_tokens = set(
            self.tokenize(query_text)
        )

        key_tokens = set(
            self.tokenize(key_text)
        )

        value_tokens = set(
            self.tokenize(value_text)
        )

        if not query_tokens:

            return score

        key_matches = (
            query_tokens & key_tokens
        )

        value_matches = (
            query_tokens & value_tokens
        )

        # Key matches are more important than value matches.

        if key_matches:

            score += (
                len(key_matches)
                / len(query_tokens)
            ) * 12.0

        if value_matches:

            score += (
                len(value_matches)
                / len(query_tokens)
            ) * 6.0

        # ----------------------------------------------------
        # Combined semantic-ish overlap
        # ----------------------------------------------------

        combined_matches = (
            query_tokens
            & (key_tokens | value_tokens)
        )

        if combined_matches:

            score += (
                len(combined_matches)
                / len(query_tokens)
            ) * 4.0

        return round(
            score,
            4
        )

    # ========================================================
    # FIND RELEVANT MEMORIES
    # ========================================================

    def find_relevant(
        self,
        query: Any,
        memories=None,
        limit: int = 5,
        min_score: float = 1.0
    ) -> List[Dict[str, Any]]:
        """
        Return memories ranked by relevance.
        """

        if query is None:

            return []

        query = str(
            query
        ).strip()

        if not query:

            return []

        # ----------------------------------------------------
        # Get memories
        # ----------------------------------------------------

        if memories is None:

            if not self.connected():

                return []

            try:

                memories = (
                    self.memory_manager.recall_all()
                )

            except Exception as e:

                print(
                    "[MemoryRelevance] "
                    f"Memory read warning: {e}"
                )

                return []

        if not memories:

            return []

        results = []

        # ----------------------------------------------------
        # Score every memory
        # ----------------------------------------------------

        for item in memories:

            parsed = self.extract_memory(
                item
            )

            if parsed is None:

                continue

            key, value = parsed

            score = self.score_memory(
                query,
                key,
                value
            )

            if score < min_score:

                continue

            results.append(
                {
                    "key": key,
                    "value": value,
                    "score": score,
                }
            )

        # ----------------------------------------------------
        # Sort
        # ----------------------------------------------------

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # ----------------------------------------------------
        # Limit
        # ----------------------------------------------------

        return results[:max(
            0,
            int(limit)
        )]

    # ========================================================
    # BUILD RELEVANT CONTEXT
    # ========================================================

    def build_context(
        self,
        query: Any,
        memories=None,
        limit: int = 5,
        min_score: float = 1.0
    ) -> Dict[str, Any]:
        """
        Build a clean context object for Brain.
        """

        query = (
            str(query).strip()
            if query is not None
            else ""
        )

        relevant = self.find_relevant(
            query=query,
            memories=memories,
            limit=limit,
            min_score=min_score
        )

        return {
            "available": self.connected(),
            "query": query,
            "memories": relevant,
            "count": len(relevant),
        }

    # ========================================================
    # FORMAT CONTEXT
    # ========================================================

    @staticmethod
    def format_context(
        context: Dict[str, Any]
    ) -> str:
        """
        Convert relevant memories into readable text.
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

            if not isinstance(
                item,
                dict
            ):

                continue

            key = item.get(
                "key",
                ""
            )

            value = item.get(
                "value",
                ""
            )

            if not key:

                continue

            lines.append(
                f"{key}: {value}"
            )

        return "\n".join(
            lines
        )

    # ========================================================
    # HEALTH
    # ========================================================

    def health(self) -> Dict[str, bool]:
        """
        Return module health.
        """

        return {
            "memory_relevance": True,
            "memory_manager_connected": (
                self.connected()
            ),
        }


# ============================================================
# STANDALONE TEST
# ============================================================

def run_memory_relevance_test():

    print()
    print("=" * 60)
    print(
        "          MYX MEMORY RELEVANCE TEST"
    )
    print("=" * 60)

    try:

        # ----------------------------------------------------
        # Fake in-memory test data
        # ----------------------------------------------------

        memories = [
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
                "favorite_editor",
                "Cursor"
            ),
        ]

        engine = MemoryRelevance(
            memory_manager=True
        )

        # ----------------------------------------------------
        # Test 1 — Connection
        # ----------------------------------------------------

        if engine.connected():

            print(
                "[1] Connection : PASS"
            )

        else:

            print(
                "[1] Connection : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 2 — Normalize
        # ----------------------------------------------------

        normalized = engine.normalize(
            "  MyX   AI!!! "
        )

        if normalized == "myx ai":

            print(
                "[2] Normalize : PASS"
            )

        else:

            print(
                "[2] Normalize : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 3 — Tokenize
        # ----------------------------------------------------

        tokens = engine.tokenize(
            "MyX AI Assistant"
        )

        if (
            "myx" in tokens
            and "assistant" in tokens
        ):

            print(
                "[3] Tokenize : PASS"
            )

        else:

            print(
                "[3] Tokenize : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 4 — Exact Relevance
        # ----------------------------------------------------

        score = engine.score_memory(
            "What is my project?",
            "project",
            "MyX AI Assistant"
        )

        if score > 0:

            print(
                "[4] Relevance Score : PASS"
            )

        else:

            print(
                "[4] Relevance Score : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 5 — Ranking
        # ----------------------------------------------------

        results = engine.find_relevant(
            query="MyX project",
            memories=memories,
            limit=3
        )

        if (
            results
            and results[0]["key"] == "project"
        ):

            print(
                "[5] Relevance Ranking : PASS"
            )

        else:

            print(
                "[5] Relevance Ranking : FAIL"
            )

            print(
                "    Results:",
                results
            )

            return False

        # ----------------------------------------------------
        # Test 6 — Context
        # ----------------------------------------------------

        context = engine.build_context(
            query="MyX project",
            memories=memories,
            limit=3
        )

        if (
            context["count"] >= 1
            and isinstance(
                context["memories"],
                list
            )
        ):

            print(
                "[6] Context Build : PASS"
            )

        else:

            print(
                "[6] Context Build : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 7 — Formatting
        # ----------------------------------------------------

        formatted = (
            engine.format_context(
                context
            )
        )

        if (
            isinstance(
                formatted,
                str
            )
            and "project:" in formatted
        ):

            print(
                "[7] Context Format : PASS"
            )

        else:

            print(
                "[7] Context Format : FAIL"
            )

            print(
                "    Context:",
                formatted
            )

            return False

        # ----------------------------------------------------
        # Test 8 — Health
        # ----------------------------------------------------

        health = engine.health()

        if (
            health["memory_relevance"] is True
            and health[
                "memory_manager_connected"
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
            "       MYX MEMORY RELEVANCE : PASS"
        )
        print("=" * 60)

        return True

    except Exception as e:

        print()
        print(
            "[MemoryRelevance Test] FAIL"
        )

        print(
            "Error:",
            e
        )

        return False


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    success = (
        run_memory_relevance_test()
    )

    raise SystemExit(
        0 if success else 1
    )
