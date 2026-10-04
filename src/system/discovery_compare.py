class DiscoveryCompare:
    """
    MYX Discovery Comparison

    Compares two discovery result lists.

    This module only analyzes discovery data.
    It does NOT launch or modify applications.
    """

    def __init__(self, start_menu_items, start_apps_items):
        self.start_menu_items = start_menu_items
        self.start_apps_items = start_apps_items

        print("[DiscoveryCompare] Initialized")

    @staticmethod
    def normalize_name(name):
        return " ".join(
            str(name).strip().lower().split()
        )

    def compare(self):
        start_menu_names = {
            self.normalize_name(item["name"])
            for item in self.start_menu_items
        }

        start_apps_names = {
            self.normalize_name(item["name"])
            for item in self.start_apps_items
        }

        both = sorted(
            start_menu_names & start_apps_names
        )

        start_menu_only = sorted(
            start_menu_names - start_apps_names
        )

        start_apps_only = sorted(
            start_apps_names - start_menu_names
        )

        return {
            "both": both,
            "start_menu_only": start_menu_only,
            "start_apps_only": start_apps_only,
        }


def main():
    from start_menu_discovery import StartMenuDiscovery
    from src.system.discovery.start_apps_discovery import StartAppsDiscovery

    start_menu = StartMenuDiscovery().discover()
    start_apps = StartAppsDiscovery().discover()

    comparison = DiscoveryCompare(
        start_menu,
        start_apps,
    ).compare()

    print()
    print("==========================================")
    print("       MYX DISCOVERY COMPARISON TEST")
    print("==========================================")

    print()
    print(
        f"Start Menu entries : {len(start_menu)}"
    )

    print(
        f"StartApps entries  : {len(start_apps)}"
    )

    print(
        f"Present in both    : "
        f"{len(comparison['both'])}"
    )

    print(
        f"Start Menu only    : "
        f"{len(comparison['start_menu_only'])}"
    )

    print(
        f"StartApps only     : "
        f"{len(comparison['start_apps_only'])}"
    )

    print()
    print("--------------- PRESENT IN BOTH ----------------")

    for name in comparison["both"]:
        print(f"- {name}")

    print()
    print("------------- START MENU ONLY ------------------")

    for name in comparison["start_menu_only"]:
        print(f"- {name}")

    print()
    print("-------------- STARTAPPS ONLY -------------------")

    for name in comparison["start_apps_only"]:
        print(f"- {name}")


if __name__ == "__main__":
    main()

