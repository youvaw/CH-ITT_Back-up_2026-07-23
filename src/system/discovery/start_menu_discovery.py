import os


class StartMenuDiscovery:
    """
    MYX Start Menu Discovery

    Discovers:
    - .lnk Windows shortcuts
    - .url web shortcuts

    This module only discovers.
    It does NOT launch anything.
    """

    def __init__(self):
        print("[StartMenuDiscovery] Initialized")

    def get_start_menu_paths(self):
        """Return available Windows Start Menu locations."""

        paths = [
            os.path.join(
                os.environ.get("ProgramData", ""),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
            ),
            os.path.join(
                os.environ.get("APPDATA", ""),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
            ),
        ]

        return [
            path
            for path in paths
            if os.path.isdir(path)
        ]

    def discover(self):
        """Discover Start Menu shortcuts."""

        applications = []

        for start_menu_path in self.get_start_menu_paths():

            for root, _, files in os.walk(start_menu_path):

                for filename in files:

                    extension = os.path.splitext(
                        filename
                    )[1].lower()

                    if extension not in (".lnk", ".url"):
                        continue

                    full_path = os.path.join(
                        root,
                        filename,
                    )

                    name = os.path.splitext(
                        filename
                    )[0].strip()

                    relative_path = os.path.relpath(
                        full_path,
                        start_menu_path,
                    )

                    item_type = (
                        "shortcut"
                        if extension == ".lnk"
                        else "url"
                    )

                    applications.append({
                        "name": name,
                        "source": "start_menu",
                        "item_type": item_type,
                        "launch_target": full_path,
                        "start_menu_path": relative_path,
                    })

        applications.sort(
            key=lambda item: item["name"].lower()
        )

        return applications


def main():
    discovery = StartMenuDiscovery()

    applications = discovery.discover()

    print()
    print("==========================================")
    print("       MYX START MENU DISCOVERY TEST")
    print("==========================================")
    print(
        f"Start Menu entries found: "
        f"{len(applications)}"
    )
    print()

    for application in applications:
        print(
            f"- {application['name']}"
            f" | Type: {application['item_type']}"
            f" | Source: {application['source']}"
        )


if __name__ == "__main__":
    main()

