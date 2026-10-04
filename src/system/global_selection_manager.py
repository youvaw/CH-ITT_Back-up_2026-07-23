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
# GLOBAL SELECTION MANAGER
# ============================================================

class GlobalSelectionManager:
    """
    MYX Global Selection Manager

    Handles candidate selection when a global search/action
    returns multiple results.

    Responsibilities:
        - Store candidates
        - Number candidates
        - Display candidate options
        - Select by number
        - Select by name
        - Handle invalid selections
        - Never execute the selected action

    This module is intentionally independent from the
    actual action executor.
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):
        self.candidates = []
        self.selected_candidate = None

        print("[GlobalSelectionManager] Initialized")

    # ========================================================
    # NORMALIZATION
    # ========================================================

    def normalize(self, value):
        if value is None:
            return ""

        return str(value).strip()

    # ========================================================
    # SET CANDIDATES
    # ========================================================

    def set_candidates(self, candidates):
        """
        Store a clean candidate list.

        Non-list values are safely converted into a list.
        """

        if candidates is None:
            self.candidates = []
            self.selected_candidate = None
            return self.candidates

        if not isinstance(candidates, list):
            candidates = [candidates]

        self.candidates = list(candidates)
        self.selected_candidate = None

        return self.candidates

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self):
        self.candidates = []
        self.selected_candidate = None

    # ========================================================
    # COUNT
    # ========================================================

    def count(self):
        return len(self.candidates)

    # ========================================================
    # HAS CANDIDATES
    # ========================================================

    def has_candidates(self):
        return self.count() > 0

    # ========================================================
    # GET CANDIDATE
    # ========================================================

    def get_candidate(self, index):
        """
        Return candidate using zero-based index.
        """

        if not isinstance(index, int):
            return None

        if index < 0:
            return None

        if index >= len(self.candidates):
            return None

        return self.candidates[index]

    # ========================================================
    # DISPLAY NAME
    # ========================================================

    def candidate_name(self, candidate):
        """
        Extract a useful display name from a candidate.

        Supports dictionaries and normal objects.
        """

        if isinstance(candidate, dict):

            for key in (
                "name",
                "display_name",
                "title",
                "path",
                "full_name",
            ):
                value = candidate.get(key)

                if value:
                    return self.normalize(value)

            return "Unknown"

        for attribute in (
            "name",
            "display_name",
            "title",
            "path",
            "full_name",
        ):
            value = getattr(candidate, attribute, None)

            if value:
                return self.normalize(value)

        return self.normalize(candidate) or "Unknown"

    # ========================================================
    # NUMBERED CANDIDATES
    # ========================================================

    def numbered_candidates(self):
        """
        Return candidates in numbered form.

        Example:

            [
                (1, candidate_a),
                (2, candidate_b)
            ]
        """

        return [
            (index + 1, candidate)
            for index, candidate in enumerate(self.candidates)
        ]

    # ========================================================
    # SELECT BY NUMBER
    # ========================================================

    def select_by_number(self, number):
        """
        Select a candidate using human-friendly numbering.

        User selection:
            1 = first candidate
            2 = second candidate
        """

        try:
            number = int(number)
        except (TypeError, ValueError):
            return None

        if number < 1:
            return None

        index = number - 1

        candidate = self.get_candidate(index)

        if candidate is None:
            return None

        self.selected_candidate = candidate

        return candidate

    # ========================================================
    # SELECT BY NAME
    # ========================================================

    def select_by_name(self, name):
        """
        Select the first candidate whose display name matches
        the supplied name.

        Matching is case-insensitive.
        """

        name = self.normalize(name).lower()

        if not name:
            return None

        for candidate in self.candidates:

            candidate_name = self.candidate_name(candidate)

            if candidate_name.lower() == name:
                self.selected_candidate = candidate
                return candidate

        return None

    # ========================================================
    # PARTIAL NAME SELECTION
    # ========================================================

    def select_by_partial_name(self, name):
        """
        Select the first candidate whose name contains
        the supplied text.
        """

        name = self.normalize(name).lower()

        if not name:
            return None

        for candidate in self.candidates:

            candidate_name = self.candidate_name(candidate)

            if name in candidate_name.lower():
                self.selected_candidate = candidate
                return candidate

        return None

    # ========================================================
    # GENERAL SELECTION
    # ========================================================

    def select(self, selection):
        """
        Automatically determine whether the selection is:

            - numeric
            - exact name
            - partial name

        """

        if selection is None:
            return None

        selection = self.normalize(selection)

        if not selection:
            return None

        # ----------------------------------------------------
        # Number selection
        # ----------------------------------------------------

        if selection.isdigit():
            return self.select_by_number(int(selection))

        # ----------------------------------------------------
        # Exact name
        # ----------------------------------------------------

        result = self.select_by_name(selection)

        if result is not None:
            return result

        # ----------------------------------------------------
        # Partial name
        # ----------------------------------------------------

        return self.select_by_partial_name(selection)

    # ========================================================
    # SELECTED CANDIDATE
    # ========================================================

    def get_selected(self):
        return self.selected_candidate

    # ========================================================
    # HAS SELECTION
    # ========================================================

    def has_selection(self):
        return self.selected_candidate is not None

    # ========================================================
    # SELECTION STATUS
    # ========================================================

    def selection_status(self):
        """
        Return a structured selection status.
        """

        if not self.has_candidates():
            return {
                "status": "empty",
                "selected": None,
                "count": 0,
            }

        if not self.has_selection():
            return {
                "status": "pending",
                "selected": None,
                "count": self.count(),
            }

        return {
            "status": "selected",
            "selected": self.selected_candidate,
            "count": self.count(),
        }

    # ========================================================
    # PRINT OPTIONS
    # ========================================================

    def print_candidates(self):
        """
        Print candidate choices for CLI/debug/testing.
        """

        if not self.has_candidates():
            print("No candidates available.")
            return

        print("\nMYX CANDIDATES")
        print("------------------------------------------")

        for number, candidate in self.numbered_candidates():

            name = self.candidate_name(candidate)

            print(f"{number}. {name}")

        print("------------------------------------------")

    # ========================================================
    # PRINT SELECTION
    # ========================================================

    def print_selection(self):
        """
        Print current selection state.
        """

        status = self.selection_status()

        print("\nMYX SELECTION STATUS")
        print("------------------------------------------")
        print("Status    :", status["status"])
        print("Candidates:", status["count"])

        if status["selected"] is not None:
            print(
                "Selected  :",
                self.candidate_name(status["selected"])
            )
        else:
            print("Selected  : None")

        print("------------------------------------------")

        return status


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("==========================================")
    print("MYX STEP 11.15 GLOBAL SELECTION TEST")
    print("==========================================")

    manager = GlobalSelectionManager()

    tests_passed = 0
    total_tests = 7

    # ========================================================
    # TEST 1
    # ========================================================

    print("\n[TEST 1] Manager Initialization")

    if isinstance(manager, GlobalSelectionManager):
        print("INITIALIZATION TEST: PASS")
        tests_passed += 1
    else:
        print("INITIALIZATION TEST: FAIL")

    # ========================================================
    # TEST 2
    # ========================================================

    print("\n[TEST 2] Candidate Storage")

    candidates = [
        {
            "name": "Google Chrome",
            "type": "application",
        },
        {
            "name": "Visual Studio Code",
            "type": "application",
        },
        {
            "name": "Calculator",
            "type": "application",
        },
    ]

    manager.set_candidates(candidates)

    if manager.count() == 3:
        print("CANDIDATE STORAGE TEST: PASS")
        tests_passed += 1
    else:
        print("CANDIDATE STORAGE TEST: FAIL")

    # ========================================================
    # TEST 3
    # ========================================================

    print("\n[TEST 3] Numbered Candidate List")

    numbered = manager.numbered_candidates()

    if (
        len(numbered) == 3
        and numbered[0][0] == 1
        and numbered[1][0] == 2
        and numbered[2][0] == 3
    ):
        print("NUMBERING TEST: PASS")
        tests_passed += 1
    else:
        print("NUMBERING TEST: FAIL")

    # ========================================================
    # TEST 4
    # ========================================================

    print("\n[TEST 4] Select By Number")

    selected = manager.select_by_number(2)

    if (
        selected is not None
        and manager.candidate_name(selected)
        == "Visual Studio Code"
    ):
        print("NUMBER SELECTION TEST: PASS")
        tests_passed += 1
    else:
        print("NUMBER SELECTION TEST: FAIL")

    # ========================================================
    # TEST 5
    # ========================================================

    print("\n[TEST 5] Select By Name")

    selected = manager.select_by_name("Calculator")

    if (
        selected is not None
        and manager.candidate_name(selected)
        == "Calculator"
    ):
        print("NAME SELECTION TEST: PASS")
        tests_passed += 1
    else:
        print("NAME SELECTION TEST: FAIL")

    # ========================================================
    # TEST 6
    # ========================================================

    print("\n[TEST 6] Invalid Selection Safety")

    selected = manager.select_by_number(99)

    if selected is None:
        print("INVALID SELECTION TEST: PASS")
        tests_passed += 1
    else:
        print("INVALID SELECTION TEST: FAIL")

    # ========================================================
    # TEST 7
    # ========================================================

    print("\n[TEST 7] Empty Candidate Safety")

    manager.clear()

    selected = manager.select_by_number(1)

    if (
        manager.count() == 0
        and selected is None
        and manager.selection_status()["status"] == "empty"
    ):
        print("EMPTY CANDIDATE TEST: PASS")
        tests_passed += 1
    else:
        print("EMPTY CANDIDATE TEST: FAIL")

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n==========================================")
    print(f"Tests passed : {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("GLOBAL SELECTION TEST: PASS")
        print("STEP 11.15 TEST PASSED")
    else:
        print("GLOBAL SELECTION TEST: FAIL")

    print("==========================================")
    
