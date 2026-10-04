import os
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# APPLICATION RESOLVER
# ============================================================

class ApplicationResolver:
    """
    Resolves the best available launch mechanism for an
    ApplicationRecord.

    This class does NOT launch applications.

    It only answers:
        "How can this application be launched?"
    """

    def __init__(self):
        print("[ApplicationResolver] Initialized")

    # --------------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------------

    def normalize(self, value):
        if value is None:
            return ""

        return str(value).strip()

    # --------------------------------------------------------
    # PATH CHECK
    # --------------------------------------------------------

    def valid_path(self, path):
        path = self.normalize(path)

        if not path:
            return False

        try:
            return os.path.exists(path)
        except Exception:
            return False

    # --------------------------------------------------------
    # EXECUTABLE CHECK
    # --------------------------------------------------------

    def resolve_executable(self, record):
        executable = self.normalize(
            getattr(record, "executable", None)
        )

        if not executable:
            return None

        # Full executable path
        if os.path.isabs(executable):
            if self.valid_path(executable):
                return {
                    "method": "executable",
                    "target": executable,
                }

            return None

        # Executable available through PATH
        return {
            "method": "executable",
            "target": executable,
        }

    # --------------------------------------------------------
    # LAUNCH TARGET CHECK
    # --------------------------------------------------------

    def resolve_launch_target(self, record):
        target = self.normalize(
            getattr(record, "launch_target", None)
        )

        if not target:
            return None

        # Existing file / shortcut / executable
        if self.valid_path(target):
            return {
                "method": "launch_target",
                "target": target,
            }

        # URL
        if target.lower().startswith(
            ("http://", "https://")
        ):
            return {
                "method": "url",
                "target": target,
            }

        return None

    # --------------------------------------------------------
    # APP ID CHECK
    # --------------------------------------------------------

    def resolve_app_id(self, record):
        app_id = self.normalize(
            getattr(record, "app_id", None)
        )

        if not app_id:
            return None

        return {
            "method": "app_id",
            "target": app_id,
        }

    # --------------------------------------------------------
    # MAIN RESOLUTION
    # --------------------------------------------------------

    def resolve(self, record):
        if record is None:
            return None

        # ----------------------------------------------------
        # 1. EXECUTABLE
        # ----------------------------------------------------

        result = self.resolve_executable(record)

        if result:
            return result

        # ----------------------------------------------------
        # 2. LAUNCH TARGET
        # ----------------------------------------------------

        result = self.resolve_launch_target(record)

        if result:
            return result

        # ----------------------------------------------------
        # 3. APP ID
        # ----------------------------------------------------

        result = self.resolve_app_id(record)

        if result:
            return result

        # ----------------------------------------------------
        # NOTHING FOUND
        # ----------------------------------------------------

        return None


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("       MYX APPLICATION RESOLVER TEST")
    print("==========================================")

    from src.system.discovery.application_record import ApplicationRecord

    resolver = ApplicationResolver()

    # --------------------------------------------------------
    # TEST 1 — executable
    # --------------------------------------------------------

    chrome = ApplicationRecord(
        name="Google Chrome",
        sources=["registry"],
        item_type="application",
        app_id="Chrome",
        launch_target=None,
        executable="chrome.exe",
        publisher="Google LLC",
        version=None,
        install_location=None,
        launchable=True,
    )

    result = resolver.resolve(chrome)

    print()
    print("Chrome resolver result:")
    print(result)

    assert result is not None
    assert result["method"] == "executable"
    assert result["target"] == "chrome.exe"

    # --------------------------------------------------------
    # TEST 2 — URL
    # --------------------------------------------------------

    node_site = ApplicationRecord(
        name="Node.js website",
        sources=["start_menu"],
        item_type="web",
        app_id=None,
        launch_target="https://nodejs.org/",
        executable=None,
        publisher=None,
        version=None,
        install_location=None,
        launchable=True,
    )

    result = resolver.resolve(node_site)

    print()
    print("Node.js website resolver result:")
    print(result)

    assert result is not None
    assert result["method"] == "url"
    assert result["target"] == "https://nodejs.org/"

    # --------------------------------------------------------
    # TEST 3 — App ID
    # --------------------------------------------------------

    calculator = ApplicationRecord(
        name="Calculator",
        sources=["start_apps"],
        item_type="application",
        app_id="Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
        launch_target=None,
        executable=None,
        publisher=None,
        version=None,
        install_location=None,
        launchable=True,
    )

    result = resolver.resolve(calculator)

    print()
    print("Calculator resolver result:")
    print(result)

    assert result is not None
    assert result["method"] == "app_id"
    assert result["target"] == (
        "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
    )

    # --------------------------------------------------------
    # TEST 4 — Nothing resolvable
    # --------------------------------------------------------

    unknown = ApplicationRecord(
        name="Unknown Application",
        sources=["test"],
        item_type="unknown",
        app_id=None,
        launch_target=None,
        executable=None,
        publisher=None,
        version=None,
        install_location=None,
        launchable=False,
    )

    result = resolver.resolve(unknown)

    print()
    print("Unknown application resolver result:")
    print(result)

    assert result is None

    # --------------------------------------------------------
    # PASS
    # --------------------------------------------------------

    print()
    print("==========================================")
    print("APPLICATION RESOLVER TEST PASSED")
    print("==========================================")
    

