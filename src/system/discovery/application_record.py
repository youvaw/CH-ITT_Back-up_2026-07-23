class ApplicationRecord:
    """
    MYX Normalized Application Record

    Represents one discovered Windows application or launchable item.

    This module only defines and validates application data.
    It does NOT discover or launch applications.
    """

    VALID_TYPES = {
        "application",
        "system_tool",
        "web",
        "shortcut",
        "unknown",
    }

    def __init__(
        self,
        name,
        normalized_name=None,
        sources=None,
        item_type="unknown",
        app_id=None,
        launch_target=None,
        executable=None,
        publisher=None,
        version=None,
        install_location=None,
        launchable=True,
    ):
        self.name = str(name).strip()

        self.normalized_name = (
            normalized_name
            if normalized_name is not None
            else self.normalize_name(self.name)
        )

        self.sources = list(sources or [])
        self.item_type = item_type
        self.app_id = app_id
        self.launch_target = launch_target
        self.executable = executable
        self.publisher = publisher
        self.version = version
        self.install_location = install_location
        self.launchable = bool(launchable)

        self.validate()

    @staticmethod
    def normalize_name(name):
        """Create a consistent comparison name."""

        return " ".join(
            str(name).strip().lower().split()
        )

    def add_source(self, source):
        """Add a discovery source without duplicates."""

        source = str(source).strip()

        if source and source not in self.sources:
            self.sources.append(source)

    def validate(self):
        """Validate the normalized record."""

        if not self.name:
            raise ValueError(
                "Application name cannot be empty."
            )

        if self.item_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid application type: "
                f"{self.item_type}"
            )

    def to_dict(self):
        """Convert the record to a dictionary."""

        return {
            "name": self.name,
            "normalized_name": self.normalized_name,
            "sources": list(self.sources),
            "item_type": self.item_type,
            "app_id": self.app_id,
            "launch_target": self.launch_target,
            "executable": self.executable,
            "publisher": self.publisher,
            "version": self.version,
            "install_location": self.install_location,
            "launchable": self.launchable,
        }

    def __repr__(self):
        return (
            "ApplicationRecord("
            f"name={self.name!r}, "
            f"type={self.item_type!r}, "
            f"sources={self.sources!r}"
            ")"
        )


def main():
    print()
    print("==========================================")
    print("      MYX APPLICATION RECORD TEST")
    print("==========================================")

    chrome = ApplicationRecord(
        name="Google Chrome",
        sources=[
            "registry",
            "start_menu",
            "start_apps",
        ],
        item_type="application",
        app_id="Chrome",
        executable="chrome.exe",
        publisher="Google LLC",
        launchable=True,
    )

    calculator = ApplicationRecord(
        name="Calculator",
        sources=[
            "start_apps",
        ],
        item_type="application",
        app_id="Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
        launchable=True,
    )

    node_website = ApplicationRecord(
        name="Node.js website",
        sources=[
            "start_menu",
            "start_apps",
        ],
        item_type="web",
        launch_target="https://nodejs.org/",
        launchable=True,
    )

    print()
    print("Chrome:")
    print(chrome.to_dict())

    print()
    print("Calculator:")
    print(calculator.to_dict())

    print()
    print("Node.js website:")
    print(node_website.to_dict())

    print()
    print("Normalization test:")
    print(
        ApplicationRecord.normalize_name(
            "  Google   Chrome  "
        )
    )

    print()
    print("Source merge test:")
    chrome.add_source("start_menu")
    chrome.add_source("registry")

    print(chrome.sources)

    print()
    print("==========================================")
    print("APPLICATION RECORD TEST PASSED")
    print("==========================================")


if __name__ == "__main__":
    main()

