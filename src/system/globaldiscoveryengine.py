import os
import sys
import time


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.system.discovery_record import DiscoveryRecord
from src.system.discovery_source_registry import DiscoverySourceRegistry


class GlobalDiscoveryEngine:
    """
    Central discovery coordinator.

    It collects discovery results from registered sources
    and normalizes them into DiscoveryRecord objects.
    """

    def __init__(self, source_registry=None):
        self.source_registry = (
            source_registry
            or DiscoverySourceRegistry()
        )

        self.records = []

        print("[GlobalDiscoveryEngine] Initialized")

    def add_record(self, record):
        if isinstance(record, DiscoveryRecord):
            self.records.append(record)
            return True

        if isinstance(record, dict):
            self.records.append(
                DiscoveryRecord(
                    name=record.get("name", ""),
                    item_type=record.get(
                        "item_type",
                        record.get("type", "unknown")
                    ),
                    source=record.get("source"),
                    location=record.get("location"),
                    target=record.get("target"),
                    executable=record.get("executable"),
                    capabilities=record.get("capabilities", []),
                    metadata=record.get("metadata", {}),
                    launchable=record.get("launchable", False),
                )
            )
            return True

        return False

    def discover(self, providers=None):
        """
        providers:
            Optional dictionary of source_id -> callable.

        The engine does not hard-code individual applications.
        """

        providers = providers or {}

        discovered = []
        started = time.time()

        for source_id in self.source_registry.list_sources(
            enabled_only=True
        ):
            provider = providers.get(source_id)

            if provider is None:
                continue

            try:
                result = provider()

                if result is None:
                    continue

                if isinstance(result, DiscoveryRecord):
                    result = [result]

                if isinstance(result, dict):
                    result = [result]

                for item in result:
                    if self.add_record(item):
                        discovered.append(self.records[-1])

            except Exception as error:
                print(
                    f"[Discovery Warning] "
                    f"{source_id}: {error}"
                )

        elapsed = round(time.time() - started, 4)

        return {
            "success": True,
            "count": len(discovered),
            "records": discovered,
            "time": elapsed,
        }

    def register_provider(self, source_id, provider):
        if not callable(provider):
            return False

        if not self.source_registry.has(source_id):
            return False

        if not hasattr(self, "_providers"):
            self._providers = {}

        self._providers[source_id] = provider
        return True

    def run(self):
        providers = getattr(self, "_providers", {})
        return self.discover(providers)

    def clear(self):
        self.records.clear()

    def count(self):
        return len(self.records)

    def list_records(self):
        return list(self.records)

    def get_by_type(self, item_type):
        item_type = str(item_type).strip().lower()

        return [
            record
            for record in self.records
            if record.item_type == item_type
        ]

    def status(self):
        return {
            "engine": "global_discovery",
            "ready": True,
            "source_count": self.source_registry.count(),
            "record_count": self.count(),
        }


if __name__ == "__main__":
    print("=" * 55)
    print("    MYX STEP 10.3 GLOBAL DISCOVERY ENGINE TEST")
    print("=" * 55)

    engine = GlobalDiscoveryEngine()

    def fake_apps():
        return [
            DiscoveryRecord(
                name="Google Chrome",
                item_type="application",
                source="test",
                executable="chrome.exe",
                capabilities=["open", "launch"],
                launchable=True,
            ),
            DiscoveryRecord(
                name="Visual Studio Code",
                item_type="application",
                source="test",
                executable="code.exe",
                capabilities=["open", "launch"],
                launchable=True,
            ),
        ]

    def fake_files():
        return [
            DiscoveryRecord(
                name="Python Tutorial.pdf",
                item_type="file",
                source="test",
                capabilities=["find", "open", "locate"],
            )
        ]

    engine.register_provider("applications", fake_apps)
    engine.register_provider("files", fake_files)

    print("\n[TEST 1] Engine Initialization")

    test1 = engine.status()["ready"] is True

    print("Engine ready:", engine.status()["ready"])
    print(
        "INITIALIZATION TEST:",
        "PASS" if test1 else "FAIL"
    )

    print("\n[TEST 2] Provider Registration")

    test2 = (
        "applications" in getattr(
            engine,
            "_providers",
            {}
        )
    )

    print("Providers:", list(
        getattr(engine, "_providers", {}).keys()
    ))

    print(
        "PROVIDER TEST:",
        "PASS" if test2 else "FAIL"
    )

    print("\n[TEST 3] Discovery Run")

    result = engine.run()

    test3 = (
        result["success"]
        and result["count"] == 3
    )

    print("Records discovered:", result["count"])
    print(
        "DISCOVERY RUN TEST:",
        "PASS" if test3 else "FAIL"
    )

    print("\n[TEST 4] Type Filtering")

    applications = engine.get_by_type("application")

    test4 = len(applications) == 2

    print(
        "Applications:",
        [item.name for item in applications]
    )

    print(
        "TYPE FILTER TEST:",
        "PASS" if test4 else "FAIL"
    )

    print("\n[TEST 5] Engine Status")

    status = engine.status()

    test5 = (
        status["ready"]
        and status["record_count"] == 3
    )

    print("Status:", status)

    print(
        "STATUS TEST:",
        "PASS" if test5 else "FAIL"
    )

    tests = [test1, test2, test3, test4, test5]
    passed = sum(tests)

    print("\n" + "-" * 55)
    print(f"Tests passed : {passed}/5")

    if passed == 5:
        print("GLOBAL DISCOVERY ENGINE TEST: PASS")
        print("STEP 10.3 TEST PASSED")
    else:
        print("GLOBAL DISCOVERY ENGINE TEST: FAIL")
        print("STEP 10.3 TEST FAILED")

    print("-" * 55)
    
