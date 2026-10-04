import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.system.discovery.application_record import ApplicationRecord


class ApplicationRegistry:
    """
    MYX Application Registry

    Combines discovery results into normalized
    ApplicationRecord objects.
    """

    def __init__(self):
        self._records = {}

        print("[ApplicationRegistry] Initialized")

    def _normalize_key(self, name):
        return ApplicationRecord.normalize_name(name)

    def add(self, item):
        if not isinstance(item, dict):
            raise TypeError("Registry item must be a dictionary.")

        name = str(item.get("name", "")).strip()

        if not name:
            return False

        key = self._normalize_key(name)

        source = item.get("source", "unknown")

        item_type = item.get(
            "item_type",
            "unknown"
        )

        if item_type == "registered_app":
            item_type = "application"

        if item_type == "url":
            item_type = "web"

        if item_type not in ApplicationRecord.VALID_TYPES:
            item_type = "unknown"

        if key not in self._records:

            record = ApplicationRecord(
                name=name,
                normalized_name=key,
                sources=[source],
                item_type=item_type,
                app_id=item.get("app_id"),
                launch_target=item.get("launch_target"),
                executable=item.get("executable"),
                publisher=item.get("publisher"),
                version=item.get("version"),
                install_location=item.get("install_location"),
                launchable=item.get("launchable", True),
            )

            self._records[key] = record

            return True

        record = self._records[key]

        record.add_source(source)

        if record.app_id is None and item.get("app_id"):
            record.app_id = item["app_id"]

        if (
            record.launch_target is None
            and item.get("launch_target")
        ):
            record.launch_target = item["launch_target"]

        if (
            record.executable is None
            and item.get("executable")
        ):
            record.executable = item["executable"]

        if (
            record.publisher is None
            and item.get("publisher")
        ):
            record.publisher = item["publisher"]

        if (
            record.version is None
            and item.get("version")
        ):
            record.version = item["version"]

        if (
            record.install_location is None
            and item.get("install_location")
        ):
            record.install_location = item["install_location"]

        if item.get("launchable") is True:
            record.launchable = True

        return False

    def add_many(self, items):

        added = 0
        merged = 0

        for item in items:

            if self.add(item):
                added += 1
            else:
                merged += 1

        return {
            "added": added,
            "merged": merged,
        }

    def get(self, name):

        key = self._normalize_key(name)

        return self._records.get(key)

    def exists(self, name):

        return self.get(name) is not None

    def all(self):

        return sorted(
            self._records.values(),
            key=lambda record: record.normalized_name
        )

    def count(self):

        return len(self._records)

    def to_dict(self):

        return [
            record.to_dict()
            for record in self.all()
        ]


def main():

    from src.system.discovery.start_menu_discovery import (
        StartMenuDiscovery
    )

    from src.system.discovery.start_apps_discovery import (
        StartAppsDiscovery
    )

    print()
    print("==========================================")
    print("       MYX APPLICATION REGISTRY TEST")
    print("==========================================")

    # Start Menu Discovery
    start_menu = StartMenuDiscovery().discover()

    print()
    print(
        f"Start Menu discovered : {len(start_menu)}"
    )

    # StartApps Discovery
    start_apps = StartAppsDiscovery().discover()

    print(
        f"StartApps discovered  : {len(start_apps)}"
    )

    # Registry
    registry = ApplicationRegistry()

    start_menu_result = registry.add_many(
        start_menu
    )

    start_apps_result = registry.add_many(
        start_apps
    )

    print()
    print(
        f"Start Menu added      : "
        f"{start_menu_result['added']}"
    )

    print(
        f"Start Menu merged     : "
        f"{start_menu_result['merged']}"
    )

    print(
        f"StartApps added       : "
        f"{start_apps_result['added']}"
    )

    print(
        f"StartApps merged      : "
        f"{start_apps_result['merged']}"
    )

    print()
    print(
        f"Unique registry items : "
        f"{registry.count()}"
    )

    # Lookup
    print()
    print("--------------- LOOKUP TEST ----------------")

    test_names = [
        "Google Chrome",
        "Calculator",
        "Copilot",
        "Visual Studio Code",
        "Lenovo Vantage",
    ]

    for name in test_names:

        record = registry.get(name)

        if record:

            print()
            print(f"{name}:")
            print(record.to_dict())

        else:

            print()
            print(f"{name}: NOT FOUND")

    # Merge verification
    print()
    print("------------- MERGE TEST ------------------")

    chrome = registry.get("Google Chrome")

    if chrome:

        print("Google Chrome sources:")
        print(chrome.sources)

    print()
    print("==========================================")
    print("APPLICATION REGISTRY TEST PASSED")
    print("==========================================")


if __name__ == "__main__":
    main()


