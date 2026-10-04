import os
import sys
import subprocess
import webbrowser


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# APPLICATION LAUNCHER
# ============================================================

class ApplicationLauncher:
    """
    Generic Windows application launcher.

    The launcher receives a resolved launch instruction and
    executes it.

    It does NOT know about:
        Chrome
        Calculator
        VS Code
        Lenovo Vantage
        Copilot
        etc.

    Therefore newly discovered applications can use the same
    launcher without adding application-specific functions.
    """

    def __init__(self):
        print("[ApplicationLauncher] Initialized")

    # --------------------------------------------------------
    # EXECUTABLE
    # --------------------------------------------------------

    def launch_executable(self, target):
        target = str(target).strip()

        if not target:
            return {
                "success": False,
                "method": "executable",
                "target": target,
                "message": "Executable target is empty.",
            }

        try:
            subprocess.Popen(
                target,
                shell=True
            )

            return {
                "success": True,
                "method": "executable",
                "target": target,
                "message": f"Started {target}.",
            }

        except Exception as e:
            return {
                "success": False,
                "method": "executable",
                "target": target,
                "message": f"Unable to start executable: {e}",
            }

    # --------------------------------------------------------
    # FILE / SHORTCUT / LAUNCH TARGET
    # --------------------------------------------------------

    def launch_target(self, target):
        target = str(target).strip()

        if not target:
            return {
                "success": False,
                "method": "launch_target",
                "target": target,
                "message": "Launch target is empty.",
            }

        try:
            os.startfile(target)

            return {
                "success": True,
                "method": "launch_target",
                "target": target,
                "message": f"Opened {target}.",
            }

        except Exception as e:
            return {
                "success": False,
                "method": "launch_target",
                "target": target,
                "message": f"Unable to open target: {e}",
            }

    # --------------------------------------------------------
    # URL
    # --------------------------------------------------------

    def launch_url(self, target):
        target = str(target).strip()

        if not target:
            return {
                "success": False,
                "method": "url",
                "target": target,
                "message": "URL target is empty.",
            }

        try:
            webbrowser.open(target)

            return {
                "success": True,
                "method": "url",
                "target": target,
                "message": f"Opened {target}.",
            }

        except Exception as e:
            return {
                "success": False,
                "method": "url",
                "target": target,
                "message": f"Unable to open URL: {e}",
            }

    # --------------------------------------------------------
    # WINDOWS APP ID
    # --------------------------------------------------------

    def launch_app_id(self, target):
        target = str(target).strip()

        if not target:
            return {
                "success": False,
                "method": "app_id",
                "target": target,
                "message": "App ID is empty.",
            }

        try:
            command = [
                "explorer.exe",
                f"shell:AppsFolder\\{target}",
            ]

            subprocess.Popen(command)

            return {
                "success": True,
                "method": "app_id",
                "target": target,
                "message": f"Launched application ID {target}.",
            }

        except Exception as e:
            return {
                "success": False,
                "method": "app_id",
                "target": target,
                "message": f"Unable to launch App ID: {e}",
            }

    # --------------------------------------------------------
    # GENERIC LAUNCH
    # --------------------------------------------------------

    def launch(self, instruction):
        """
        Execute a resolver instruction.

        Expected format:

        {
            "method": "...",
            "target": "..."
        }
        """

        if not instruction:
            return {
                "success": False,
                "method": None,
                "target": None,
                "message": "No launch instruction provided.",
            }

        method = str(
            instruction.get("method", "")
        ).strip().lower()

        target = instruction.get("target")

        if method == "executable":
            return self.launch_executable(target)

        if method == "launch_target":
            return self.launch_target(target)

        if method == "url":
            return self.launch_url(target)

        if method == "app_id":
            return self.launch_app_id(target)

        return {
            "success": False,
            "method": method,
            "target": target,
            "message": f"Unsupported launch method: {method}",
        }


# ============================================================
# ISOLATED AUTOMATED TESTS
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("       MYX APPLICATION LAUNCHER TEST")
    print("==========================================")

    launcher = ApplicationLauncher()

    # --------------------------------------------------------
    # TEST 1 — URL dispatch
    #
    # We do NOT actually open a browser.
    # Replace launch_url temporarily with a fake function.
    # --------------------------------------------------------

    url_calls = []

    def fake_url(target):
        url_calls.append(target)

        return {
            "success": True,
            "method": "url",
            "target": target,
            "message": "TEST URL",
        }

    launcher.launch_url = fake_url

    result = launcher.launch({
        "method": "url",
        "target": "https://example.com/",
    })

    print()
    print("URL dispatch result:")
    print(result)

    assert result["success"] is True
    assert result["method"] == "url"
    assert result["target"] == "https://example.com/"
    assert url_calls == ["https://example.com/"]

    # --------------------------------------------------------
    # TEST 2 — executable dispatch
    #
    # No real process is started.
    # --------------------------------------------------------

    executable_calls = []

    def fake_executable(target):
        executable_calls.append(target)

        return {
            "success": True,
            "method": "executable",
            "target": target,
            "message": "TEST EXECUTABLE",
        }

    launcher.launch_executable = fake_executable

    result = launcher.launch({
        "method": "executable",
        "target": "test_application.exe",
    })

    print()
    print("Executable dispatch result:")
    print(result)

    assert result["success"] is True
    assert result["method"] == "executable"
    assert result["target"] == "test_application.exe"
    assert executable_calls == ["test_application.exe"]

    # --------------------------------------------------------
    # TEST 3 — launch target dispatch
    #
    # No real file/shortcut is opened.
    # --------------------------------------------------------

    target_calls = []

    def fake_target(target):
        target_calls.append(target)

        return {
            "success": True,
            "method": "launch_target",
            "target": target,
            "message": "TEST TARGET",
        }

    launcher.launch_target = fake_target

    result = launcher.launch({
        "method": "launch_target",
        "target": r"C:\Test\TestApp.lnk",
    })

    print()
    print("Launch target dispatch result:")
    print(result)

    assert result["success"] is True
    assert result["method"] == "launch_target"
    assert result["target"] == r"C:\Test\TestApp.lnk"
    assert target_calls == [r"C:\Test\TestApp.lnk"]

    # --------------------------------------------------------
    # TEST 4 — App ID dispatch
    #
    # No real Windows application is launched.
    # --------------------------------------------------------

    app_id_calls = []

    def fake_app_id(target):
        app_id_calls.append(target)

        return {
            "success": True,
            "method": "app_id",
            "target": target,
            "message": "TEST APP ID",
        }

    launcher.launch_app_id = fake_app_id

    result = launcher.launch({
        "method": "app_id",
        "target": "Test.App_123!App",
    })

    print()
    print("App ID dispatch result:")
    print(result)

    assert result["success"] is True
    assert result["method"] == "app_id"
    assert result["target"] == "Test.App_123!App"
    assert app_id_calls == ["Test.App_123!App"]

    # --------------------------------------------------------
    # TEST 5 — Unknown method
    # --------------------------------------------------------

    result = launcher.launch({
        "method": "unknown_method",
        "target": "something",
    })

    print()
    print("Unknown method result:")
    print(result)

    assert result["success"] is False
    assert result["method"] == "unknown_method"

    # --------------------------------------------------------
    # TEST 6 — Empty instruction
    # --------------------------------------------------------

    result = launcher.launch(None)

    print()
    print("Empty instruction result:")
    print(result)

    assert result["success"] is False
    assert result["method"] is None

    # --------------------------------------------------------
    # PASS
    # --------------------------------------------------------

    print()
    print("==========================================")
    print("APPLICATION LAUNCHER TEST PASSED")
    print("==========================================")
    
