# -*- coding: utf-8 -*-

"""
MYX Transmission Route Table

Defines the high-level gears/routes used by the
Transmission Engine.

This file does NOT execute tools.
It only describes where a request should go.
"""


class RouteTable:
    """
    Central route/gear definitions for MYX.
    """

    ROUTES = {
        "G1": {
            "name": "LOCAL_SYSTEM",
            "description": "Fast local system operations",
            "target": "system",
        },
        "G2": {
            "name": "LOCAL_TOOLS",
            "description": "Local registered tools",
            "target": "tools",
        },
        "G3": {
            "name": "APPLICATION_WEB",
            "description": "Applications and web operations",
            "target": "web",
        },
        "G4": {
            "name": "FILES_ADVANCED_TOOLS",
            "description": "Files and advanced tool operations",
            "target": "files",
        },
        "G5": {
            "name": "AI_CONVERSATION",
            "description": "AI conversation and reasoning",
            "target": "ai",
        },
        "R": {
            "name": "RECOVERY",
            "description": "Fallback and recovery route",
            "target": "recovery",
        },
    }

    @classmethod
    def get(cls, gear):
        """
        Return route information for a gear.
        """
        gear = str(gear or "").strip().upper()
        return cls.ROUTES.get(gear)

    @classmethod
    def exists(cls, gear):
        """
        Check whether a gear exists.
        """
        return cls.get(gear) is not None

    @classmethod
    def all_routes(cls):
        """
        Return all configured routes.
        """
        return dict(cls.ROUTES)


if __name__ == "__main__":
    print("=" * 60)
    print("MYX TRANSMISSION ROUTE TABLE TEST")
    print("=" * 60)

    table = RouteTable()

    for gear in ("G1", "G2", "G3", "G4", "G5", "R"):
        print()
        print(gear, "->", table.get(gear))

    print()
    print("G1 EXISTS:", table.exists("G1"))
    print("G9 EXISTS:", table.exists("G9"))

    print()
    print("ROUTE TABLE : PASS")
    print("=" * 60)
