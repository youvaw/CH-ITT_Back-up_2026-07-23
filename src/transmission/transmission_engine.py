# -*- coding: utf-8 -*-

"""
MYX Transmission Engine

Flow:

    User Command
          ↓
    Gear Selector
          ↓
    Route Table
          ↓
    Transmission Decision

Important:
    This module does NOT execute tools.
    It only creates a routing decision.
"""

from .gear_selector import GearSelector


class TransmissionEngine:

    def __init__(self):
        self.gear_selector = GearSelector()
        print("[TransmissionEngine] Initialized")

    def route(self, command):
        """
        Analyze a command and return the transmission decision.
        """

        command = str(command or "").strip()

        if not command:
            return {
                "success": False,
                "stage": "transmission",
                "gear": "R",
                "route": "RECOVERY",
                "target": "recovery",
                "command": "",
                "reason": "Empty command",
            }

        selection = self.gear_selector.select(command)

        return {
            "success": True,
            "stage": "transmission",
            "command": command,
            "gear": selection["gear"],
            "route": selection["route"],
            "target": selection["target"],
            "reason": selection["reason"],
        }

    def inspect(self, command):
        """
        Alias for route().

        Useful when another module wants to inspect
        the routing decision without implying execution.
        """
        return self.route(command)


if __name__ == "__main__":

    print("=" * 70)
    print("MYX TRANSMISSION ENGINE TEST")
    print("=" * 70)

    engine = TransmissionEngine()

    tests = [
        "battery status",
        "memory usage",
        "open google",
        "search youtube",
        "find file report.txt",
        "explain quantum physics",
        "hello myx",
        "",
    ]

    for command in tests:

        result = engine.route(command)

        print()
        print("COMMAND :", repr(command))
        print("GEAR    :", result["gear"])
        print("ROUTE   :", result["route"])
        print("TARGET  :", result["target"])
        print("REASON  :", result["reason"])

    print()
    print("TRANSMISSION ENGINE : PASS")
    print("=" * 70)
