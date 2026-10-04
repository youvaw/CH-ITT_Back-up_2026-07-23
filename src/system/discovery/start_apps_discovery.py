import subprocess


class StartAppsDiscovery:
    """
    MYX Windows StartApps Discovery

    Discovers applications registered with Windows StartApps.

    This module only discovers.
    It does NOT launch anything.
    """

    def __init__(self):
        print("[StartAppsDiscovery] Initialized")

    def discover(self):
        """Discover Windows StartApps using PowerShell."""

        applications = []

        command = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-StartApps | Select-Object Name, AppID | ConvertTo-Json -Compress"
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True,
            )

            output = result.stdout.strip()

            if not output:
                return applications

            import json

            data = json.loads(output)

            if isinstance(data, dict):
                data = [data]

            for item in data:
                name = str(item.get("Name", "")).strip()
                app_id = str(item.get("AppID", "")).strip()

                if not name:
                    continue

                applications.append({
                    "name": name,
                    "source": "start_apps",
                    "item_type": "registered_app",
                    "app_id": app_id,
                })

            applications.sort(
                key=lambda item: item["name"].lower()
            )

            return applications

        except subprocess.CalledProcessError as e:
            print("[StartAppsDiscovery] PowerShell error:")
            print(e.stderr)
            return []

        except Exception as e:
            print(
                f"[StartAppsDiscovery] Discovery error: {e}"
            )
            return []


def main():
    discovery = StartAppsDiscovery()

    applications = discovery.discover()

    print()
    print("==========================================")
    print("        MYX STARTAPPS DISCOVERY TEST")
    print("==========================================")
    print(
        f"StartApps entries found: "
        f"{len(applications)}"
    )
    print()

    for application in applications:
        print(
            f"- {application['name']}"
            f" | Type: {application['item_type']}"
            f" | AppID: {application['app_id']}"
        )


if __name__ == "__main__":
    main()

