import winreg


class AppDiscovery:
    def __init__(self):
        print("[AppDiscovery] Initialized")

    def discover_registry(self):
        """Discover software registered in Windows Uninstall registry."""

        registry_paths = [
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
            ),
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            ),
            (
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
            ),
        ]

        applications = []

        for hive, registry_path in registry_paths:
            try:
                with winreg.OpenKey(hive, registry_path) as uninstall_key:

                    subkey_count = winreg.QueryInfoKey(uninstall_key)[0]

                    for index in range(subkey_count):
                        try:
                            subkey_name = winreg.EnumKey(
                                uninstall_key,
                                index,
                            )

                            with winreg.OpenKey(
                                uninstall_key,
                                subkey_name,
                            ) as app_key:

                                def read_value(name):
                                    try:
                                        return winreg.QueryValueEx(
                                            app_key,
                                            name,
                                        )[0]
                                    except (FileNotFoundError, OSError):
                                        return ""

                                name = str(
                                    read_value("DisplayName")
                                ).strip()

                                if not name:
                                    continue

                                record = {
                                    "name": name,
                                    "source": "registry",
                                    "item_type": "installed_software",
                                    "app_id": subkey_name,
                                    "version": str(
                                        read_value("DisplayVersion")
                                    ).strip(),
                                    "publisher": str(
                                        read_value("Publisher")
                                    ).strip(),
                                    "install_location": str(
                                        read_value("InstallLocation")
                                    ).strip(),
                                    "launch_target": str(
                                        read_value("DisplayIcon")
                                    ).strip(),
                                }

                                applications.append(record)

                        except (FileNotFoundError, OSError):
                            continue

            except (FileNotFoundError, OSError):
                continue

        return applications


if __name__ == "__main__":
    discovery = AppDiscovery()

    apps = discovery.discover_registry()

    print()
    print("==========================================")
    print("       MYX REGISTRY DISCOVERY TEST")
    print("==========================================")
    print(f"Installed software found: {len(apps)}")
    print()

    for app in apps[:20]:
        print(
            f"- {app['name']}"
            f" | Version: {app['version'] or 'N/A'}"
            f" | Publisher: {app['publisher'] or 'N/A'}"
        )
        
