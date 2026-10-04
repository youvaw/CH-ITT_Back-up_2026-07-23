# -*- coding: utf-8 -*-

"""
MYX Launch Events

All launch events are kept separate from the animation engine.
This allows Development Mode changes without touching launch logic.
"""

from src.gui.launch_config import EVENTS


def get_event(second):
    return EVENTS.get(second, "")


def get_all_events():
    return EVENTS.copy()


def print_events():
    print()
    print("========== MYX LAUNCH EVENTS ==========")

    for second in sorted(EVENTS.keys(), reverse=True):
        text = EVENTS[second]

        if text:
            print(f"{second:02d}  {text}")
        else:
            print(f"{second:02d}")

    print("=======================================")
    