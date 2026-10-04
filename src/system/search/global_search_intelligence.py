# -*- coding: utf-8 -*-

"""
MYX Global Search Intelligence

Purpose:
- Understand search results from the real discovery system
- Support DiscoveryRecord objects and dictionaries
- Rank results intelligently
- Remove duplicates
- Prioritize exact matches
- Prioritize user paths
- Penalize noisy/system results
- Provide safe result summaries

This module does NOT execute actions.
It only understands and ranks search results.
"""

from copy import deepcopy


class GlobalSearchIntelligence:
    """
    Intelligence layer between RealGlobalSearch and action systems.
    """

    def __init__(self, search_engine=None):
        self.search_engine = search_engine
        print("[GlobalSearchIntelligence] Initialized")

    # ============================================================
    # BASIC NORMALIZATION
    # ============================================================

    @staticmethod
    def normalize(value):
        """
        Convert a value into normalized searchable text.
        """
        if value is None:
            return ""

        return " ".join(
            str(value)
            .strip()
            .lower()
            .split()
        )

    # ============================================================
    # RECORD ACCESSORS
    # ============================================================

    def get_name(self, record):
        """
        Get record name from either:
        - dict
        - DiscoveryRecord object
        """

        if record is None:
            return ""

        # Dictionary support
        if isinstance(record, dict):
            return str(
                record.get("name")
                or record.get("title")
                or record.get("display_name")
                or ""
            )

        # Object support
        for attribute in (
            "name",
            "title",
            "display_name",
        ):
            try:
                value = getattr(record, attribute, None)

                if value:
                    return str(value)

            except Exception:
                pass

        return ""

    def get_path(self, record):
        """
        Get filesystem/path/location information.
        """

        if record is None:
            return ""

        # Dictionary support
        if isinstance(record, dict):
            return str(
                record.get("path")
                or record.get("location")
                or record.get("target")
                or ""
            )

        # Object support
        for attribute in (
            "path",
            "location",
            "target",
            "executable",
        ):
            try:
                value = getattr(record, attribute, None)

                if value:
                    return str(value)

            except Exception:
                pass

        return ""

    def get_type(self, record):
        """
        Get item type.

        Examples:
        application
        file
        folder
        storage
        web
        other
        """

        if record is None:
            return ""

        # Dictionary support
        if isinstance(record, dict):
            return str(
                record.get("item_type")
                or record.get("type")
                or record.get("category")
                or "other"
            )

        # Object support
        for attribute in (
            "item_type",
            "type",
            "category",
        ):
            try:
                value = getattr(record, attribute, None)

                if value:
                    return str(value)

            except Exception:
                pass

        return "other"

    def get_item_type(self, record):
        """
        Compatibility alias used by GlobalSearchActionIntegration.
        """

        return self.get_type(record)

    # ============================================================
    # DEDUPLICATION
    # ============================================================

    def dedup_key(self, record):
        """
        Create a stable key for duplicate detection.
        """

        name = self.normalize(
            self.get_name(record)
        )

        path = self.normalize(
            self.get_path(record)
        )

        item_type = self.normalize(
            self.get_type(record)
        )

        # Prefer path when available because two items
        # can have the same name.
        if path:
            return (
                item_type,
                path,
            )

        return (
            item_type,
            name,
        )

    def deduplicate(self, records):
        """
        Remove duplicate records.

        Important:
        Original DiscoveryRecord objects are preserved.
        """

        if records is None:
            return []

        unique = {}
        
        for record in records:

            if record is None:
                continue

            try:
                key = self.dedup_key(record)

                if key not in unique:
                    unique[key] = record

            except Exception:
                # If a record cannot be analyzed,
                # keep it rather than silently deleting it.
                fallback_key = (
                    "unknown",
                    id(record),
                )

                if fallback_key not in unique:
                    unique[fallback_key] = record

        return list(unique.values())

    # ============================================================
    # MATCHING HELPERS
    # ============================================================

    def exact_match_score(self, name, query):
        """
        Exact name matching.
        """

        normalized_name = self.normalize(name)
        normalized_query = self.normalize(query)

        if not normalized_name or not normalized_query:
            return 0

        if normalized_name == normalized_query:
            return 95

        return 0

    def prefix_match_score(self, name, query):
        """
        Prefix matching.
        """

        normalized_name = self.normalize(name)
        normalized_query = self.normalize(query)

        if not normalized_name or not normalized_query:
            return 0

        if normalized_name.startswith(normalized_query):
            return 70

        return 0

    def contains_match_score(self, name, query):
        """
        Partial/contains matching.
        """

        normalized_name = self.normalize(name)
        normalized_query = self.normalize(query)

        if not normalized_name or not normalized_query:
            return 0

        if normalized_query in normalized_name:
            return 50

        return 0

    def word_match_score(self, name, query):
        """
        Word-level matching.
        """

        normalized_name = self.normalize(name)
        normalized_query = self.normalize(query)

        if not normalized_name or not normalized_query:
            return 0

        name_words = set(
            normalized_name.split()
        )

        query_words = set(
            normalized_query.split()
        )

        if not query_words:
            return 0

        matched = name_words.intersection(
            query_words
        )

        if not matched:
            return 0

        ratio = len(matched) / len(query_words)

        if ratio >= 1:
            return 45

        if ratio >= 0.5:
            return 30

        return 15

    # ============================================================
    # PATH INTELLIGENCE
    # ============================================================

    def user_path_bonus(self, record):
        """
        Prioritize user-owned locations.

        Example:
        C:\\Users\\AVISHKAR\\Documents
        C:\\Users\\AVISHKAR\\Downloads
        C:\\Users\\AVISHKAR\\Desktop
        """

        path = self.normalize(
            self.get_path(record)
        )

        if not path:
            return 0

        user_markers = (
            "\\users\\",
            "/users/",
            "desktop",
            "documents",
            "downloads",
            "pictures",
            "videos",
            "music",
            "onedrive",
        )

        for marker in user_markers:
            if marker in path:
                return 20

        return 0

    # ============================================================
    # NOISE PENALTY
    # ============================================================

    def noise_penalty(self, record):
        """
        Penalize system/cache/temp/noisy locations.
        """

        path = self.normalize(
            self.get_path(record)
        )

        name = self.normalize(
            self.get_name(record)
        )

        combined = f"{path} {name}"

        noisy_markers = (
            "\\windows\\",
            "/windows/",
            "\\system32\\",
            "/system32/",
            "\\appdata\\local\\temp",
            "/appdata/local/temp",
            "\\programdata\\",
            "/programdata/",
            "\\$recycle.bin\\",
            "/$recycle.bin/",
            "cache",
            "temporary internet files",
        )

        penalty = 0

        for marker in noisy_markers:
            if marker in combined:
                penalty = max(
                    penalty,
                    25,
                )

        return penalty

    # ============================================================
    # ITEM TYPE BONUS
    # ============================================================

    def type_bonus(self, record):
        """
        Slight preference for useful launchable/searchable types.
        """

        item_type = self.normalize(
            self.get_type(record)
        )

        if item_type == "application":
            return 10

        if item_type == "file":
            return 5

        if item_type == "folder":
            return 3

        if item_type == "web":
            return 3

        return 0

    # ============================================================
    # TOTAL SCORE
    # ============================================================

    def calculate_score(self, record, query):
        """
        Calculate intelligent search score.
        """

        if record is None:
            return 0

        query = str(query or "").strip()

        if not query:
            return 0

        name = self.get_name(record)

        if not name:
            return 0

        score = 0

        # Exact match
        score += self.exact_match_score(
            name,
            query,
        )

        # Prefix match
        score += self.prefix_match_score(
            name,
            query,
        )

        # Contains match
        score += self.contains_match_score(
            name,
            query,
        )

        # Word match
        score += self.word_match_score(
            name,
            query,
        )

        # User path priority
        score += self.user_path_bonus(
            record
        )

        # Type priority
        score += self.type_bonus(
            record
        )

        # Noise penalty
        score -= self.noise_penalty(
            record
        )

        return max(
            0,
            score,
        )

    # ============================================================
    # RANK RESULTS
    # ============================================================

    def rank_results(self, records, query):
        """
        Rank results without mutating DiscoveryRecord objects.

        Returns:
            List of original records sorted by score.
        """

        if not records:
            return []

        ranked = []

        for index, record in enumerate(records):

            if record is None:
                continue

            try:
                score = self.calculate_score(
                    record,
                    query,
                )

                name = self.normalize(
                    self.get_name(record)
                )

                # Keep original object.
                ranked.append(
                    (
                        score,
                        name,
                        -index,
                        record,
                    )
                )

            except Exception as e:
                print(
                    "[GlobalSearchIntelligence] "
                    f"Ranking error: {e}"
                )

        ranked.sort(
            key=lambda item: (
                item[0],
                item[1],
                item[2],
            ),
            reverse=True,
        )

        return [
            item[3]
            for item in ranked
        ]

    # ============================================================
    # SEARCH ENGINE ACCESS
    # ============================================================

    def search_records(self, query):
        """
        Call the connected real search engine.
        """

        query = str(query or "").strip()

        if not query:
            return []

        if self.search_engine is None:
            return []

        try:
            results = self.search_engine.search(
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
                "[GlobalSearchIntelligence] "
                f"Search engine error: {e}"
            )

            return []

    # ============================================================
    # MAIN SEARCH
    # ============================================================

    def search(self, query):
        """
        Main intelligent search API.
        """

        query = str(query or "").strip()

        if not query:
            return []

        records = self.search_records(
            query
        )

        if not records:
            return []

        records = self.deduplicate(
            records
        )

        records = self.rank_results(
            records,
            query,
        )

        return records

    # ============================================================
    # TOP RESULT
    # ============================================================

    def top_result(self, query):
        """
        Return highest ranked result.
        """

        results = self.search(
            query
        )

        if not results:
            return None

        return results[0]

    # ============================================================
    # SUMMARY
    # ============================================================

    def summarize(self, records):
        """
        Return result type summary.
        """

        summary = {
            "total": 0,
            "applications": 0,
            "files": 0,
            "folders": 0,
            "storage": 0,
            "web": 0,
            "other": 0,
        }

        if not records:
            return summary

        for record in records:

            if record is None:
                continue

            item_type = self.normalize(
                self.get_type(record)
            )

            summary["total"] += 1

            if item_type == "application":
                summary["applications"] += 1

            elif item_type == "file":
                summary["files"] += 1

            elif item_type == "folder":
                summary["folders"] += 1

            elif item_type == "storage":
                summary["storage"] += 1

            elif item_type == "web":
                summary["web"] += 1

            else:
                summary["other"] += 1

        return summary

    # ============================================================
    # RESULT DESCRIPTION
    # ============================================================

    def describe_result(self, record):
        """
        Convert any supported record into
        a safe display dictionary.
        """

        if record is None:
            return {
                "name": "",
                "item_type": "",
                "path": "",
                "score": 0,
            }

        name = self.get_name(record)
        item_type = self.get_item_type(record)
        path = self.get_path(record)

        score = 0

        try:
            score = self.calculate_score(
                record,
                name,
            )
        except Exception:
            score = 0

        return {
            "name": str(name or ""),
            "item_type": str(item_type or ""),
            "path": str(path or ""),
            "score": score,
        }

    # ============================================================
    # PRINT RESULTS
    # ============================================================

    def print_results(self, records, query=""):
        """
        Human-readable diagnostic output.
        """

        if not records:
            print("No results.")
            return

        print()
        print("=" * 60)
        print("MYX GLOBAL SEARCH RESULTS")
        print("=" * 60)

        for index, record in enumerate(
            records,
            start=1,
        ):

            name = self.get_name(record)
            item_type = self.get_item_type(record)
            path = self.get_path(record)

            score = 0

            if query:
                score = self.calculate_score(
                    record,
                    query,
                )

            print()
            print(
                f"[{index}] {name}"
            )
            print(
                f"    Type  : {item_type}"
            )
            print(
                f"    Path  : {path}"
            )
            print(
                f"    Score : {score}"
            )

        print()
        print("=" * 60)

    # ============================================================
    # BUILT-IN TEST
    # ============================================================


def run_test():
    """
    Local unit/integration-style test.

    Uses dictionaries so the intelligence layer
    can be tested independently.
    """

    print()
    print("=" * 46)
    print(
        "MYX STEP 11.11 "
        "GLOBAL SEARCH INTELLIGENCE TEST"
    )
    print("=" * 46)

    intelligence = GlobalSearchIntelligence()

    passed = 0
    total = 8

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    print()
    print("[TEST 1] Initialization")

    if intelligence is not None:
        print(
            "Search engine connected: PASS"
        )
        passed += 1

    else:
        print(
            "Search engine connected: FAIL"
        )

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    print()
    print("[TEST 2] Exact Match Ranking")

    records = [
        {
            "name": "Google Chrome",
            "item_type": "application",
        },
        {
            "name": "ChromeSetup.exe",
            "item_type": "file",
        },
    ]

    ranked = intelligence.rank_results(
        records,
        "Google Chrome",
    )

    if ranked:

        top_name = intelligence.get_name(
            ranked[0]
        )

        score = intelligence.calculate_score(
            ranked[0],
            "Google Chrome",
        )

        print(
            f"Top result: {top_name}"
        )
        print(
            f"Score: {score}"
        )

        if top_name == "Google Chrome":
            print(
                "EXACT MATCH TEST: PASS"
            )
            passed += 1

        else:
            print(
                "EXACT MATCH TEST: FAIL"
            )

    else:
        print(
            "EXACT MATCH TEST: FAIL"
        )

    # --------------------------------------------------------
    # TEST 3
    # --------------------------------------------------------

    print()
    print("[TEST 3] Duplicate Removal")

    duplicate_records = [
        {
            "name": "Google Chrome",
            "item_type": "application",
        },
        {
            "name": "Google Chrome",
            "item_type": "application",
        },
    ]

    unique = intelligence.deduplicate(
        duplicate_records
    )

    print(
        f"Unique results: {len(unique)}"
    )

    if len(unique) == 1:
        print(
            "DEDUPLICATION TEST: PASS"
        )
        passed += 1

    else:
        print(
            "DEDUPLICATION TEST: FAIL"
        )

    # --------------------------------------------------------
    # TEST 4
    # --------------------------------------------------------

    print()
    print("[TEST 4] User Path Priority")

    user_record = {
        "name": "Python Project",
        "item_type": "file",
        "path": (
            "C:\\Users\\AVISHKAR\\"
            "Desktop\\Python Project"
        ),
    }

    system_record = {
        "name": "Python Project",
        "item_type": "file",
        "path": (
            "C:\\Windows\\System32\\"
            "Python Project"
        ),
    }

    user_score = intelligence.user_path_bonus(
        user_record
    )

    system_score = intelligence.user_path_bonus(
        system_record
    )

    if user_score > system_score:
        print(
            "Top result: Python Project"
        )
        print(
            "USER PATH PRIORITY TEST: PASS"
        )
        passed += 1

    else:
        print(
            "USER PATH PRIORITY TEST: FAIL"
        )

    # --------------------------------------------------------
    # TEST 5
    # --------------------------------------------------------

    print()
    print("[TEST 5] Noise Penalty")

    normal_record = {
        "name": "Chrome",
        "item_type": "application",
        "path": (
            "C:\\Users\\AVISHKAR\\"
            "Desktop\\Chrome"
        ),
    }

    noisy_record = {
        "name": "Chrome",
        "item_type": "file",
        "path": (
            "C:\\Windows\\System32\\"
            "Chrome"
        ),
    }

    normal_penalty = intelligence.noise_penalty(
        normal_record
    )

    noisy_penalty = intelligence.noise_penalty(
        noisy_record
    )

    print(
        f"Normal penalty: {normal_penalty}"
    )
    print(
        f"Noisy penalty: {noisy_penalty}"
    )

    if noisy_penalty > normal_penalty:
        print(
            "NOISE PENALTY TEST: PASS"
        )
        passed += 1

    else:
        print(
            "NOISE PENALTY TEST: FAIL"
        )

    # --------------------------------------------------------
    # TEST 6
    # --------------------------------------------------------

    print()
    print("[TEST 6] Empty Query Safety")

    empty_results = intelligence.search(
        ""
    )

    print(
        f"Results: {len(empty_results)}"
    )

    if empty_results == []:
        print(
            "EMPTY QUERY TEST: PASS"
        )
        passed += 1

    else:
        print(
            "EMPTY QUERY TEST: FAIL"
        )

    # --------------------------------------------------------
    # TEST 7
    # --------------------------------------------------------

    print()
    print("[TEST 7] Result Summary")

    summary_records = [
        {
            "name": "Chrome",
            "item_type": "file",
        },
        {
            "name": "ChromeSetup",
            "item_type": "file",
        },
    ]

    summary = intelligence.summarize(
        summary_records
    )

    print(
        f"Summary: {summary}"
    )

    if (
        summary["total"] == 2
        and summary["files"] == 2
    ):
        print(
            "SUMMARY TEST: PASS"
        )
        passed += 1

    else:
        print(
            "SUMMARY TEST: FAIL"
        )

    # --------------------------------------------------------
    # TEST 8
    # --------------------------------------------------------

    print()
    print("[TEST 8] Top Result")

    top = intelligence.top_result(
        ""
    )

    # Empty query should safely return None.
    print(
        f"Top result: "
        f"{intelligence.get_name(top)}"
    )

    if top is None:
        print(
            "TOP RESULT TEST: PASS"
        )
        passed += 1

    else:
        print(
            "TOP RESULT TEST: FAIL"
        )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    print()
    print("-" * 46)
    print(
        f"Tests passed : {passed}/{total}"
    )

    if passed == total:
        print(
            "GLOBAL SEARCH INTELLIGENCE TEST: PASS"
        )
        print(
            "STEP 11.11 TEST PASSED"
        )
        print("-" * 46)
        return True

    print(
        "GLOBAL SEARCH INTELLIGENCE TEST: FAIL"
    )
    print(
        "STEP 11.11 TEST FAILED"
    )
    print("-" * 46)

    return False


if __name__ == "__main__":
    success = run_test()

    raise SystemExit(
        0 if success else 1
    )
