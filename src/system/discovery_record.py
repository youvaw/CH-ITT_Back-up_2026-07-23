import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class DiscoveryRecord:
    """
    MYX Global Discovery Record

    Represents any discoverable resource:
    application, file, folder, Windows feature,
    hardware, online service, etc.
    """

    VALID_TYPES = {
        "application",
        "file",
        "folder",
        "windows",
        "hardware",
        "service",
        "online",
        "unknown",
    }

    def __init__(
        self,
        name,
        item_type="unknown",
        source=None,
        location=None,
        target=None,
        executable=None,
        capabilities=None,
        metadata=None,
        launchable=False,
    ):
        self.name = self._normalize(name)
        self.normalized_name = self.name.lower()

        self.item_type = (
            item_type
            if item_type in self.VALID_TYPES
            else "unknown"
        )

        self.source = source
        self.location = location
        self.target = target
        self.executable = executable

        self.capabilities = list(capabilities or [])
        self.metadata = dict(metadata or {})

        self.launchable = bool(launchable)

    def add_capability(self, capability):
        capability = self._normalize(capability).lower()

        if capability and capability not in self.capabilities:
            self.capabilities.append(capability)

    def has_capability(self, capability):
        capability = self._normalize(capability).lower()
        return capability in self.capabilities

    def to_dict(self):
        return {
            "name": self.name,
            "normalized_name": self.normalized_name,
            "item_type": self.item_type,
            "source": self.source,
            "location": self.location,
            "target": self.target,
            "executable": self.executable,
            "capabilities": list(self.capabilities),
            "metadata": dict(self.metadata),
            "launchable": self.launchable,
        }

    def describe(self):
        return (
            f"{self.name} "
            f"[{self.item_type}] "
            f"capabilities={self.capabilities}"
        )

    @staticmethod
    def _normalize(value):
        if value is None:
            return ""

        return str(value).strip()


if __name__ == "__main__":
    print("=" * 50)
    print("    MYX STEP 10.1 DISCOVERY RECORD TEST")
    print("=" * 50)

    # TEST 1
    print("\n[TEST 1] Application Record")

    chrome = DiscoveryRecord(
        name="Google Chrome",
        item_type="application",
        source="start_apps",
        executable="chrome.exe",
        capabilities=["open", "launch", "search"],
        metadata={
            "publisher": "Google LLC"
        },
        launchable=True,
    )

    print(chrome.to_dict())

    test1 = (
        chrome.name == "Google Chrome"
        and chrome.item_type == "application"
        and chrome.launchable is True
    )

    print(
        "APPLICATION RECORD TEST:",
        "PASS" if test1 else "FAIL"
    )

    # TEST 2
    print("\n[TEST 2] File Record")

    pdf = DiscoveryRecord(
        name="Python Tutorial.pdf",
        item_type="file",
        source="file_index",
        location=r"C:\Users\AVISHKAR\Documents",
        target=r"C:\Users\AVISHKAR\Documents\Python Tutorial.pdf",
        capabilities=["find", "locate", "open"],
        metadata={
            "category": "pdf",
            "extension": ".pdf",
        },
    )

    print(pdf.to_dict())

    test2 = (
        pdf.name == "Python Tutorial.pdf"
        and pdf.item_type == "file"
        and pdf.has_capability("open")
    )

    print(
        "FILE RECORD TEST:",
        "PASS" if test2 else "FAIL"
    )

    # TEST 3
    print("\n[TEST 3] Capability Management")

    pdf.add_capability("show")
    pdf.add_capability("open")

    test3 = (
        pdf.has_capability("show")
        and pdf.capabilities.count("open") == 1
    )

    print("Capabilities:", pdf.capabilities)
    print(
        "CAPABILITY TEST:",
        "PASS" if test3 else "FAIL"
    )

    # TEST 4
    print("\n[TEST 4] Normalization")

    test4_record = DiscoveryRecord(
        name="   Visual Studio Code   ",
        item_type="application",
    )

    print("Name:", test4_record.name)
    print("Normalized:", test4_record.normalized_name)

    test4 = (
        test4_record.name == "Visual Studio Code"
        and test4_record.normalized_name == "visual studio code"
    )

    print(
        "NORMALIZATION TEST:",
        "PASS" if test4 else "FAIL"
    )

    # TEST 5
    print("\n[TEST 5] Invalid Type Safety")

    invalid = DiscoveryRecord(
        name="Unknown Resource",
        item_type="something_invalid",
    )

    print("Stored type:", invalid.item_type)

    test5 = invalid.item_type == "unknown"

    print(
        "TYPE SAFETY TEST:",
        "PASS" if test5 else "FAIL"
    )

    tests = [
        test1,
        test2,
        test3,
        test4,
        test5,
    ]

    passed = sum(tests)

    print("\n" + "-" * 50)
    print(f"Tests passed : {passed}/5")

    if passed == 5:
        print("DISCOVERY RECORD TEST: PASS")
        print("STEP 10.1 TEST PASSED")
    else:
        print("DISCOVERY RECORD TEST: FAIL")
        print("STEP 10.1 TEST FAILED")

    print("-" * 50)
    
