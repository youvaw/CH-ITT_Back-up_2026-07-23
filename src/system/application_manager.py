import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.discovery.application_registry import ApplicationRegistry
from src.system.discovery.application_resolver import ApplicationResolver
from src.system.application_launcher import ApplicationLauncher


class ApplicationManager:
    """
    MYX Application Manager

    Pipeline:
        Discovery
            ↓
        Registry
            ↓
        Resolver
            ↓
        Launcher
    """

    def __init__(
        self,
        registry=None,
        resolver=None,
        launcher=None,
    ):
        self.registry = registry or ApplicationRegistry()
        self.resolver = resolver or ApplicationResolver()
        self.launcher = launcher or ApplicationLauncher()

        print("[ApplicationManager] Initialized")

    def normalize(self, value):
        if value is None:
            return ""

        return " ".join(str(value).strip().lower().split())

    def find_application(self, name):
        """
        Find an application from the registry.
        """

        query = self.normalize(name)

        if not query:
            return None

        # Exact normalized-name lookup
        records = getattr(self.registry, "records", None)

        if isinstance(records, dict):
            if query in records:
                return records[query]

            # Safe fallback search
            for key, record in records.items():
                if self.normalize(key) == query:
                    return record

                record_name = getattr(
                    record,
                    "name",
                    None
                )

                if self.normalize(record_name) == query:
                    return record

        # Registry may expose a lookup method
        lookup = getattr(self.registry, "get", None)

        if callable(lookup):
            try:
                result = lookup(query)

                if result is not None:
                    return result

            except Exception:
                pass

        return None

    def resolve_application(self, name):
        """
        Find application and resolve its launch instruction.
        """

        record = self.find_application(name)

        if record is None:
            return {
                "success": False,
                "stage": "registry",
                "application": name,
                "instruction": None,
                "message": f"Application not found: {name}",
            }

        instruction = self.resolver.resolve(record)

        if instruction is None:
            return {
                "success": False,
                "stage": "resolver",
                "application": name,
                "instruction": None,
                "message": f"Unable to resolve launch target: {name}",
            }

        return {
            "success": True,
            "stage": "resolver",
            "application": name,
            "instruction": instruction,
            "message": "Application resolved successfully.",
        }

    def launch_application(self, name):
        """
        Complete pipeline:

        application name
                ↓
        registry lookup
                ↓
        resolver
                ↓
        launcher
        """

        resolved = self.resolve_application(name)

        if not resolved["success"]:
            return resolved

        result = self.launcher.launch(
            resolved["instruction"]
        )

        return {
            "success": result.get("success", False),
            "stage": "launcher",
            "application": name,
            "instruction": resolved["instruction"],
            "launch_result": result,
            "message": result.get(
                "message",
                "Launch completed."
            ),
        }


# ==========================================================
# STEP 8 ISOLATED TEST
# ==========================================================

class MockRegistry:
    """
    Fake registry for isolated testing.
    No real application discovery required.
    """

    def __init__(self):
        self.records = {
            "test application": TestRecord(
                name="Test Application",
                executable="test_application.exe",
            )
        }


class TestRecord:
    def __init__(
        self,
        name,
        executable=None,
        launch_target=None,
        app_id=None,
    ):
        self.name = name
        self.executable = executable
        self.launch_target = launch_target
        self.app_id = app_id


class MockResolver:
    def resolve(self, record):
        return {
            "method": "executable",
            "target": record.executable,
        }


class MockLauncher:
    def launch(self, instruction):
        return {
            "success": True,
            "method": instruction["method"],
            "target": instruction["target"],
            "message": "TEST LAUNCH SUCCESS",
        }


def run_test():

    print("\n==========================================")
    print("       MYX APPLICATION MANAGER TEST")
    print("==========================================")

    manager = ApplicationManager(
        registry=MockRegistry(),
        resolver=MockResolver(),
        launcher=MockLauncher(),
    )

    print("\n[1] Find application")

    record = manager.find_application(
        "Test Application"
    )

    print(record.__dict__ if record else None)

    assert record is not None
    assert record.name == "Test Application"

    print("PASS")

    print("\n[2] Resolve application")

    resolved = manager.resolve_application(
        "Test Application"
    )

    print(resolved)

    assert resolved["success"] is True
    assert resolved["instruction"]["method"] == "executable"

    print("PASS")

    print("\n[3] Launch application")

    result = manager.launch_application(
        "Test Application"
    )

    print(result)

    assert result["success"] is True
    assert result["stage"] == "launcher"
    assert result["launch_result"]["message"] == "TEST LAUNCH SUCCESS"

    print("PASS")

    print("\n[4] Unknown application")

    unknown = manager.launch_application(
        "Application That Does Not Exist"
    )

    print(unknown)

    assert unknown["success"] is False
    assert unknown["stage"] == "registry"

    print("PASS")

    print("\n==========================================")
    print("   APPLICATION MANAGER TEST PASSED")
    print("==========================================")


if __name__ == "__main__":
    run_test()
    
