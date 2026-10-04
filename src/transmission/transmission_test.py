# -*- coding: utf-8 -*-

"""
MYX Transmission Integration Test

Verifies:

    Command
       ↓
    Gear Selector
       ↓
    Route Table
       ↓
    Transmission Decision

No tool execution.
No AI call.
No Brain connection.
No GlobalActionPipeline connection.
"""

from .transmission_engine import TransmissionEngine


def run_tests():
    print("=" * 70)
    print("MYX TRANSMISSION INTEGRATION TEST")
    print("=" * 70)

    engine = TransmissionEngine()

    tests = [
        ("battery status", "G1", "LOCAL_SYSTEM", "system"),
        ("memory usage", "G1", "LOCAL_SYSTEM", "system"),
        ("open google", "G3", "APPLICATION_WEB", "web"),
        ("search youtube", "G3", "APPLICATION_WEB", "web"),
        ("find file report.txt", "G4", "FILES_ADVANCED_TOOLS", "files"),
        ("explain quantum physics", "G5", "AI_CONVERSATION", "ai"),
        ("hello myx", "G5", "AI_CONVERSATION", "ai"),
        ("", "R", "RECOVERY", "recovery"),
    ]

    passed = 0
    total = len(tests)

    for command, expected_gear, expected_route, expected_target in tests:

        result = engine.route(command)

        gear_ok = result["gear"] == expected_gear
        route_ok = result["route"] == expected_route
        target_ok = result["target"] == expected_target

        test_passed = gear_ok and route_ok and target_ok

        if test_passed:
            passed += 1

        status = "PASS" if test_passed else "FAIL"

        print()
        print(f"[{status}] {repr(command)}")
        print("       Expected Gear   :", expected_gear)
        print("       Actual Gear     :", result["gear"])
        print("       Expected Route  :", expected_route)
        print("       Actual Route    :", result["route"])
        print("       Expected Target :", expected_target)
        print("       Actual Target   :", result["target"])

    print()
    print("=" * 70)
    print("Tests passed :", f"{passed}/{total}")
    print("=" * 70)

    if passed == total:
        print("TRANSMISSION INTEGRATION : PASS")
        return True

    print("TRANSMISSION INTEGRATION : FAIL")
    return False


if __name__ == "__main__":
    run_tests()
