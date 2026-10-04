# -*- coding: utf-8 -*-

"""
MYX Transmission Gear Selector

Purpose:
    Decide which MYX transmission gear should handle a request.

Important:
    This module ONLY selects a gear.
    It does NOT execute anything.
"""

from .route_table import RouteTable


class GearSelector:

    def __init__(self):
        self.route_table = RouteTable()

    def select(self, command):
        """
        Select a transmission gear from a user command.
        """

        command = str(command or "").strip().lower()

        if not command:
            return self._result("R", "Empty command")

        # G1 - Local system
        if any(word in command for word in (
            "battery",
            "cpu",
            "processor",
            "ram",
            "memory",
            "disk",
            "storage",
            "system status",
            "system health",
            "system information",
        )):
            return self._result("G1", "Local system request")

        # G2 - Local tools
        if any(word in command for word in (
            "tool",
            "clipboard",
            "screenshot",
            "calculate",
        )):
            return self._result("G2", "Local tool request")

        # G3 - Application / Web
        if any(word in command for word in (
            "open google",
            "open youtube",
            "search web",
            "search google",
            "search youtube",
            "browser",
            "website",
            "open chrome",
        )):
            return self._result("G3", "Application or web request")

        # G4 - Files / advanced tools
        if any(word in command for word in (
            "open file",
            "find file",
            "search file",
            "folder",
            "document",
            "create file",
            "delete file",
        )):
            return self._result("G4", "File request")

        # G5 - AI conversation
        if any(word in command for word in (
            "explain",
            "what is",
            "who is",
            "how does",
            "why does",
            "tell me",
            "help me understand",
            "write",
            "summarize",
        )):
            return self._result("G5", "AI conversation request")

        # Default → AI conversation
        return self._result("G5", "General conversation")

    def _result(self, gear, reason):
        route = self.route_table.get(gear)

        return {
            "gear": gear,
            "route": route["name"] if route else None,
            "target": route["target"] if route else None,
            "reason": reason,
        }


if __name__ == "__main__":

    print("=" * 60)
    print("MYX TRANSMISSION GEAR SELECTOR TEST")
    print("=" * 60)

    selector = GearSelector()

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
        result = selector.select(command)

        print()
        print("COMMAND :", repr(command))
        print("GEAR    :", result["gear"])
        print("ROUTE   :", result["route"])
        print("TARGET  :", result["target"])
        print("REASON  :", result["reason"])

    print()
    print("GEAR SELECTOR : PASS")
    print("=" * 60)
