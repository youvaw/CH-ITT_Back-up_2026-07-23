# -*- coding: utf-8 -*-

"""
MYX OFFICIAL LAUNCH

Command:

    python -m src.gui.launch

Flow:

    Launch Animation
          ↓
    MYX IS AWAKENING
          ↓
    SYSTEM ONLINE
          ↓
    Existing MYX Login
          ↓
    Dashboard
"""

import os
import sys
import traceback


# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SRC_DIR = os.path.dirname(CURRENT_DIR)

PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from src.gui.launch_animation import run_launch_animation
from src.gui.launch_events import print_events


# ---------------------------------------------------------
# START EXISTING MYX SYSTEM
# ---------------------------------------------------------

def start_myx():
    print()
    print("=" * 55)
    print("MYX SYSTEM ONLINE")
    print("=" * 55)

    try:
        from src.gui.main import main

        print("[MYX] Starting existing Login System...")
        main()

    except Exception:
        print()
        print("=" * 55)
        print("MYX STARTUP ERROR")
        print("=" * 55)

        traceback.print_exc()

        print("=" * 55)


# ---------------------------------------------------------
# LAUNCH
# ---------------------------------------------------------

def main():
    print()
    print("=" * 60)
    print("              MYX")
    print("         FIRST AWAKENING")
    print("=" * 60)

    print_events()

    print()
    print("[MYX] Launch sequence starting...")

    run_launch_animation(
        on_complete=start_myx
    )


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
    