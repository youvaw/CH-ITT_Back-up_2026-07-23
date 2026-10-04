import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class DiscoverySourceRegistry:
    """
    Registry of MYX discovery sources.

    This stores discovery providers, not discovered items.
    """

    DEFAULT_SOURCES = {
        "applications": {
            "name": "Application Discovery",
            "module": "src.system.discovery.application_registry",
            "enabled": True,
        },
        "start_menu": {
            "name": "Start Menu Discovery",
            "module": "src.system.discovery.start_menu_discovery",
            "enabled": True,
        },
        "start_apps": {
            "name": "Windows StartApps Discovery",
            "module": "src.system.discovery.start_apps_discovery",
            "enabled": True,
        },
        "storage": {
            "name": "Storage Discovery",
            "module": "src.system.storage.storage_discovery",
            "enabled": True,
        },
        "files": {
            "name": "File System Discovery",
            "module": "src.system.file_system_service",
            "enabled": True,
        },
    }

    def __init__(self, sources=None):
        self.sources = dict(
            sources if sources is not None else self.DEFAULT_SOURCES
        )

        print("[DiscoverySourceRegistry] Initialized")

    def register(self, source_id, name, module=None, enabled=True):
        source_id = self._normalize(source_id)

        if not source_id:
            return False

        self.sources[source_id] = {
            "name": self._normalize(name),
            "module": self._normalize(module),
            "enabled": bool(enabled),
        }

        return True

    def unregister(self, source_id):
        source_id = self._normalize(source_id)

        if source_id in self.sources:
            del self.sources[source_id]
            return True

        return False

    def has(self, source_id):
        return self._normalize(source_id) in self.sources

    def get(self, source_id):
        return self.sources.get(self._normalize(source_id))

    def list_sources(self, enabled_only=False):
        if not enabled_only:
            return list(self.sources.keys())

        return [
            source_id
            for source_id, source in self.sources.items()
            if source.get("enabled", False)
        ]

    def count(self):
        return len(self.sources)

    def enabled_count(self):
        return len(self.list_sources(enabled_only=True))

    def describe(self, source_id):
        source = self.get(source_id)

        if source is None:
            return None

        return dict(source)

    def report(self):
        return {
            "total": self.count(),
            "enabled": self.enabled_count(),
            "sources": self.list_sources(),
        }

    @staticmethod
    def _normalize(value):
        if value is None:
            return ""

        return str(value).strip()


if __name__ == "__main__":
    print("=" * 55)
    print("    MYX STEP 10.2 DISCOVERY SOURCE REGISTRY TEST")
    print("=" * 55)

    registry = DiscoverySourceRegistry()

    print("\n[TEST 1] Registry Initialization")

    test1 = registry.count() >= 5

    print("Sources discovered:", registry.count())
    print(
        "INITIALIZATION TEST:",
        "PASS" if test1 else "FAIL"
    )

    print("\n[TEST 2] Source Lookup")

    application_source = registry.get("applications")

    test2 = (
        application_source is not None
        and application_source.get("enabled") is True
    )

    print("Application source:", application_source)
    print(
        "LOOKUP TEST:",
        "PASS" if test2 else "FAIL"
    )

    print("\n[TEST 3] Source Registration")

    registered = registry.register(
        "hardware",
        "Hardware Discovery",
        "src.system.hardware_discovery",
        True,
    )

    test3 = (
        registered
        and registry.has("hardware")
    )

    print("Hardware registered:", registry.has("hardware"))
    print(
        "REGISTRATION TEST:",
        "PASS" if test3 else "FAIL"
    )

    print("\n[TEST 4] Enabled Sources")

    enabled = registry.list_sources(enabled_only=True)

    test4 = len(enabled) >= 6

    print("Enabled sources:", enabled)
    print(
        "ENABLED SOURCE TEST:",
        "PASS" if test4 else "FAIL"
    )

    print("\n[TEST 5] Registry Report")

    report = registry.report()

    test5 = (
        report["total"] >= 6
        and report["enabled"] >= 6
    )

    print("Report:", report)
    print(
        "REPORT TEST:",
        "PASS" if test5 else "FAIL"
    )

    tests = [test1, test2, test3, test4, test5]
    passed = sum(tests)

    print("\n" + "-" * 55)
    print(f"Tests passed : {passed}/5")

    if passed == 5:
        print("DISCOVERY SOURCE REGISTRY TEST: PASS")
        print("STEP 10.2 TEST PASSED")
    else:
        print("DISCOVERY SOURCE REGISTRY TEST: FAIL")
        print("STEP 10.2 TEST FAILED")

    print("-" * 55)
    


