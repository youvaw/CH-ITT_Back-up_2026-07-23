"""
CHITT AI
Master Test Runner
"""

import traceback


def run_test(name, function):

    print(f"\nTesting : {name}")

    try:

        function()

        print(f"[PASS] {name}")

    except Exception as e:

        print(f"[FAIL] {name}")

        print(e)

        traceback.print_exc()


# ----------------------------

def test_config():

    from tests.test_config import config 

    return config


def test_commands():

    from tests.test_commands import run

    run()


def test_system():

    import tests.test_system


def test_intent():

    import tests.test_intent_engine


def test_registry():

    import tests.test_registry 


# ----------------------------

print("=" * 60)

print("CHITT v0.1 MASTER TEST")

print("=" * 60)

run_test("Config", test_config)

run_test("Commands", test_commands)

run_test("System", test_system)

run_test("Intent", test_intent)

run_test("Registry", test_registry)

print("\n")

print("=" * 60)

print("Testing Finished")

print("=" * 60)

