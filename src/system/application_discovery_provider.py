# ============================================================
# MYX - APPLICATION DISCOVERY PROVIDER
# STEP 11.1
# ============================================================

import json
import os
import subprocess
import sys
from typing import Any, Dict, List


# ------------------------------------------------------------
# PROJECT PATH
# ------------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------

from src.system.discovery.application_registry import ApplicationRegistry
from src.system.discovery_record import DiscoveryRecord


# ============================================================
# APPLICATION DISCOVERY PROVIDER
# ============================================================

class ApplicationDiscoveryProvider:

    def __init__(self, registry=None):
        self.registry = registry or ApplicationRegistry()

        self.records: List[DiscoveryRecord] = []
        self.ready = True

        print("[ApplicationDiscoveryProvider] Initialized")

    # ========================================================
    # NORMALIZATION HELPERS
    # ========================================================

    @staticmethod
    def _clean_name(value: Any) -> str:
        if value is None:
            return ""

        value = str(value).strip()

        if not value:
            return ""

        return value

    @staticmethod
    def _normalize_app_id(value: Any) -> str:
        if value is None:
            return ""

        return str(value).strip()

    # ========================================================
    # REGISTRY DISCOVERY
    # ========================================================

    def _discover_from_registry(self) -> List[Any]:
        """
        Read already-registered application records.

        ApplicationRegistry currently exposes:
            all()
            add()
            add_many()
            get()
            exists()
            count()
            to_dict()
        """

        if self.registry is None:
            return []

        try:
            if hasattr(self.registry, "all"):
                result = self.registry.all()
                return self._normalize_source_result(result)

        except Exception as error:
            print(
                f"[ApplicationDiscoveryProvider] "
                f"Registry discovery warning: {error}"
            )

        return []

    # ========================================================
    # WINDOWS START APPS DISCOVERY
    # ========================================================

    def _discover_from_windows(self) -> List[Dict[str, Any]]:
        """
        Discover Windows applications through Get-StartApps.

        This gives us:
            Name
            AppID

        AppID may represent:
            - packaged/UWP application
            - executable
            - Windows component
            - system tool
            - URL shortcut
        """

        powershell_command = (
            "Get-StartApps | "
            "Select-Object Name, AppID | "
            "ConvertTo-Json -Compress"
        )

        try:
            completed = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    powershell_command,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=20,
            )

            if completed.returncode != 0:
                print(
                    "[ApplicationDiscoveryProvider] "
                    f"PowerShell error: {completed.stderr.strip()}"
                )
                return []

            raw_output = completed.stdout.strip()

            if not raw_output:
                return []

            data = json.loads(raw_output)

            if isinstance(data, dict):
                data = [data]

            if not isinstance(data, list):
                return []

            results: List[Dict[str, Any]] = []

            for item in data:

                if not isinstance(item, dict):
                    continue

                name = (
                    item.get("Name")
                    or item.get("name")
                    or item.get("DisplayName")
                    or item.get("display_name")
                )

                app_id = (
                    item.get("AppID")
                    or item.get("appid")
                    or item.get("app_id")
                )

                name = self._clean_name(name)
                app_id = self._normalize_app_id(app_id)

                if not name:
                    continue

                results.append(
                    {
                        "name": name,
                        "app_id": app_id or None,
                        "source": "start_apps",
                    }
                )

            return results

        except subprocess.TimeoutExpired:
            print(
                "[ApplicationDiscoveryProvider] "
                "Get-StartApps timed out."
            )
            return []

        except json.JSONDecodeError as error:
            print(
                "[ApplicationDiscoveryProvider] "
                f"Get-StartApps JSON error: {error}"
            )
            return []

        except Exception as error:
            print(
                "[ApplicationDiscoveryProvider] "
                f"Windows discovery warning: {error}"
            )
            return []

    # ========================================================
    # SOURCE NORMALIZATION
    # ========================================================

    def _normalize_source_result(
        self,
        result: Any
    ) -> List[Dict[str, Any]]:
        """
        Normalize discovery source output into dictionaries.

        Supported:
            - dict
            - list
            - tuple
            - ApplicationRecord
            - DiscoveryRecord
            - objects exposing to_dict()
            - strings
        """

        if result is None:
            return []

        # ----------------------------------------------------
        # Dictionary container
        # ----------------------------------------------------

        if isinstance(result, dict):

            if "applications" in result:
                result = result["applications"]

            elif "results" in result:
                result = result["results"]

            elif "items" in result:
                result = result["items"]

            else:
                result = [result]

        # ----------------------------------------------------
        # Tuple / list
        # ----------------------------------------------------

        if not isinstance(result, (list, tuple)):
            result = [result]

        output: List[Dict[str, Any]] = []

        # ----------------------------------------------------
        # Individual items
        # ----------------------------------------------------

        for item in result:

            # ------------------------------------------------
            # Object with to_dict()
            # ------------------------------------------------

            if hasattr(item, "to_dict"):

                try:
                    item = item.to_dict()

                except Exception:
                    continue

            # ------------------------------------------------
            # Dictionary
            # ------------------------------------------------

            if isinstance(item, dict):

                name = (
                    item.get("name")
                    or item.get("Name")
                    or item.get("display_name")
                    or item.get("DisplayName")
                    or item.get("title")
                )

                name = self._clean_name(name)

                if not name:
                    continue

                app_id = (
                    item.get("app_id")
                    or item.get("AppID")
                    or item.get("appid")
                )

                executable = (
                    item.get("executable")
                    or item.get("Executable")
                )

                launch_target = (
                    item.get("launch_target")
                    or item.get("LaunchTarget")
                )

                publisher = (
                    item.get("publisher")
                    or item.get("Publisher")
                )

                version = (
                    item.get("version")
                    or item.get("Version")
                )

                install_location = (
                    item.get("install_location")
                    or item.get("InstallLocation")
                )

                output.append(
                    {
                        "name": name,
                        "app_id": app_id,
                        "source": item.get(
                            "source",
                            item.get(
                                "Source",
                                "application_registry"
                            )
                        ),
                        "executable": executable,
                        "launch_target": launch_target,
                        "publisher": publisher,
                        "version": version,
                        "install_location": install_location,
                    }
                )

                continue

            # ------------------------------------------------
            # String
            # ------------------------------------------------

            if isinstance(item, str):

                name = self._clean_name(item)

                if name:
                    output.append(
                        {
                            "name": name,
                            "app_id": None,
                            "source": "application_registry",
                        }
                    )

                continue

        return output

    # ========================================================
    # DISCOVERY RECORD CONVERSION
    # ========================================================

    def _to_record(
        self,
        item: Any,
        default_source: str = "start_apps"
    ) -> DiscoveryRecord | None:
        """
        Convert one application dictionary/object into
        a real DiscoveryRecord.
        """

        # ----------------------------------------------------
        # Already a DiscoveryRecord
        # ----------------------------------------------------

        if isinstance(item, DiscoveryRecord):
            return item

        # ----------------------------------------------------
        # Object -> dictionary
        # ----------------------------------------------------

        if hasattr(item, "to_dict"):

            try:
                item = item.to_dict()

            except Exception:
                return None

        # ----------------------------------------------------
        # Dictionary validation
        # ----------------------------------------------------

        if not isinstance(item, dict):
            return None

        name = (
            item.get("name")
            or item.get("Name")
            or item.get("display_name")
            or item.get("DisplayName")
        )

        name = self._clean_name(name)

        if not name:
            return None

        source = (
            item.get("source")
            or item.get("Source")
            or default_source
        )

        app_id = (
            item.get("app_id")
            or item.get("AppID")
            or item.get("appid")
        )

        executable = (
            item.get("executable")
            or item.get("Executable")
        )

        launch_target = (
            item.get("launch_target")
            or item.get("LaunchTarget")
        )

        publisher = (
            item.get("publisher")
            or item.get("Publisher")
        )

        version = (
            item.get("version")
            or item.get("Version")
        )

        install_location = (
            item.get("install_location")
            or item.get("InstallLocation")
        )

        # ----------------------------------------------------
        # Build normalized metadata
        # ----------------------------------------------------

        metadata = {
            "app_id": app_id,
        }

        if publisher:
            metadata["publisher"] = publisher

        if version:
            metadata["version"] = version

        if install_location:
            metadata["install_location"] = install_location

        # ----------------------------------------------------
        # Create DiscoveryRecord
        # ----------------------------------------------------

        try:

            record = DiscoveryRecord(
                name=name,
                item_type="application",
                source=source,
                location=install_location,
                target=launch_target,
                executable=executable,
                capabilities=[
                    "open",
                    "launch",
                    "search",
                ],
                metadata=metadata,
                launchable=True,
            )

            return record

        except Exception as error:

            print(
                "[ApplicationDiscoveryProvider] "
                f"Record conversion warning for '{name}': {error}"
            )

            return None

    # ========================================================
    # FULL DISCOVERY
    # ========================================================

    def discover(self) -> List[DiscoveryRecord]:
        """
        Discover applications from all currently available
        application sources.

        Registry is used first.
        Windows StartApps fills the inventory when registry
        data is absent or incomplete.
        """

        discovered: List[DiscoveryRecord] = []

        # ----------------------------------------------------
        # Registry source
        # ----------------------------------------------------

        registry_items = self._discover_from_registry()

        for item in registry_items:

            record = self._to_record(
                item,
                default_source="application_registry"
            )

            if record is not None:
                discovered.append(record)

        # ----------------------------------------------------
        # Windows source
        # ----------------------------------------------------

        windows_items = self._discover_from_windows()

        for item in windows_items:

            record = self._to_record(
                item,
                default_source="start_apps"
            )

            if record is not None:
                discovered.append(record)

        # ----------------------------------------------------
        # Deduplicate
        # ----------------------------------------------------

        unique: Dict[str, DiscoveryRecord] = {}

        for record in discovered:

            key = (
                getattr(record, "normalized_name", None)
                or self._clean_name(
                    getattr(record, "name", "")
                ).lower()
            )

            if not key:
                continue

            if key not in unique:
                unique[key] = record

        self.records = list(unique.values())

        return self.records

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, query: str) -> List[DiscoveryRecord]:

        query = self._clean_name(query).lower()

        if not query:
            return []

        results = []

        for record in self.records:

            name = (
                getattr(record, "normalized_name", "")
                or getattr(record, "name", "")
            )

            if query in str(name).lower():
                results.append(record)

        return results

    # ========================================================
    # STATUS
    # ========================================================

    def status(self) -> Dict[str, Any]:

        return {
            "provider": "applications",
            "ready": self.ready,
            "record_count": len(self.records),
        }

    # ========================================================
    # TESTS
    # ========================================================

    def run_tests(self) -> bool:

        print("=" * 65)
        print(
            "    MYX STEP 11.1 APPLICATION DISCOVERY PROVIDER TEST"
        )
        print("=" * 65)

        passed = 0
        total = 5

        # ----------------------------------------------------
        # TEST 1
        # ----------------------------------------------------

        print("\n[TEST 1] Provider Initialization")

        if self.registry is not None and self.ready:
            print("Registry connected: PASS")
            passed += 1
        else:
            print("Registry connected: FAIL")

        # ----------------------------------------------------
        # TEST 2
        # ----------------------------------------------------

        print("\n[TEST 2] Real Application Discovery")

        records = self.discover()

        print(
            f"Applications discovered: {len(records)}"
        )

        if len(records) > 0:
            print("DISCOVERY TEST: PASS")
            passed += 1
        else:
            print("DISCOVERY TEST: FAIL")

        # ----------------------------------------------------
        # TEST 3
        # ----------------------------------------------------

        print("\n[TEST 3] Discovery Record Conversion")

        valid_records = [
            record
            for record in records
            if isinstance(record, DiscoveryRecord)
            and getattr(record, "item_type", None)
            == "application"
        ]

        print(
            f"Valid DiscoveryRecords: {len(valid_records)}"
        )

        if (
            len(valid_records) > 0
            and len(valid_records) == len(records)
        ):
            print("RECORD CONVERSION TEST: PASS")
            passed += 1
        else:
            print("RECORD CONVERSION TEST: FAIL")

        # ----------------------------------------------------
        # TEST 4
        # ----------------------------------------------------

        print("\n[TEST 4] Application Names")

        sample = [
            record.name
            for record in records[:10]
            if getattr(record, "name", None)
        ]

        print(f"Sample applications: {sample}")

        if sample:
            print("NAME TEST: PASS")
            passed += 1
        else:
            print("NAME TEST: FAIL")

        # ----------------------------------------------------
        # TEST 5
        # ----------------------------------------------------

        print("\n[TEST 5] Provider Status")

        status = self.status()

        print(f"Status: {status}")

        if (
            status["ready"]
            and status["record_count"] == len(records)
            and status["record_count"] > 0
        ):
            print("STATUS TEST: PASS")
            passed += 1
        else:
            print("STATUS TEST: FAIL")

        # ----------------------------------------------------
        # FINAL
        # ----------------------------------------------------

        print("\n" + "-" * 65)
        print(f"Tests passed : {passed}/{total}")

        if passed == total:
            print(
                "APPLICATION DISCOVERY PROVIDER TEST: PASS"
            )
            print("STEP 11.1 TEST PASSED")
        else:
            print(
                "APPLICATION DISCOVERY PROVIDER TEST: FAIL"
            )
            print("STEP 11.1 TEST FAILED")

        print("-" * 65)

        return passed == total


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    provider = ApplicationDiscoveryProvider()

    provider.run_tests()# ============================================================
# MYX - APPLICATION DISCOVERY PROVIDER
# STEP 11.1
# ============================================================

import json
import os
import subprocess
import sys
from typing import Any, Dict, List


# ------------------------------------------------------------
# PROJECT PATH
# ------------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------

from src.system.discovery.application_registry import ApplicationRegistry
from src.system.discovery_record import DiscoveryRecord


# ============================================================
# APPLICATION DISCOVERY PROVIDER
# ============================================================

class ApplicationDiscoveryProvider:

    def __init__(self, registry=None):
        self.registry = registry or ApplicationRegistry()

        self.records: List[DiscoveryRecord] = []
        self.ready = True

        print("[ApplicationDiscoveryProvider] Initialized")

    # ========================================================
    # NORMALIZATION HELPERS
    # ========================================================

    @staticmethod
    def _clean_name(value: Any) -> str:
        if value is None:
            return ""

        value = str(value).strip()

        if not value:
            return ""

        return value

    @staticmethod
    def _normalize_app_id(value: Any) -> str:
        if value is None:
            return ""

        return str(value).strip()

    # ========================================================
    # REGISTRY DISCOVERY
    # ========================================================

    def _discover_from_registry(self) -> List[Any]:
        """
        Read already-registered application records.

        ApplicationRegistry currently exposes:
            all()
            add()
            add_many()
            get()
            exists()
            count()
            to_dict()
        """

        if self.registry is None:
            return []

        try:
            if hasattr(self.registry, "all"):
                result = self.registry.all()
                return self._normalize_source_result(result)

        except Exception as error:
            print(
                f"[ApplicationDiscoveryProvider] "
                f"Registry discovery warning: {error}"
            )

        return []

    # ========================================================
    # WINDOWS START APPS DISCOVERY
    # ========================================================

    def _discover_from_windows(self) -> List[Dict[str, Any]]:
        """
        Discover Windows applications through Get-StartApps.

        This gives us:
            Name
            AppID

        AppID may represent:
            - packaged/UWP application
            - executable
            - Windows component
            - system tool
            - URL shortcut
        """

        powershell_command = (
            "Get-StartApps | "
            "Select-Object Name, AppID | "
            "ConvertTo-Json -Compress"
        )

        try:
            completed = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    powershell_command,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=20,
            )

            if completed.returncode != 0:
                print(
                    "[ApplicationDiscoveryProvider] "
                    f"PowerShell error: {completed.stderr.strip()}"
                )
                return []

            raw_output = completed.stdout.strip()

            if not raw_output:
                return []

            data = json.loads(raw_output)

            if isinstance(data, dict):
                data = [data]

            if not isinstance(data, list):
                return []

            results: List[Dict[str, Any]] = []

            for item in data:

                if not isinstance(item, dict):
                    continue

                name = (
                    item.get("Name")
                    or item.get("name")
                    or item.get("DisplayName")
                    or item.get("display_name")
                )

                app_id = (
                    item.get("AppID")
                    or item.get("appid")
                    or item.get("app_id")
                )

                name = self._clean_name(name)
                app_id = self._normalize_app_id(app_id)

                if not name:
                    continue

                results.append(
                    {
                        "name": name,
                        "app_id": app_id or None,
                        "source": "start_apps",
                    }
                )

            return results

        except subprocess.TimeoutExpired:
            print(
                "[ApplicationDiscoveryProvider] "
                "Get-StartApps timed out."
            )
            return []

        except json.JSONDecodeError as error:
            print(
                "[ApplicationDiscoveryProvider] "
                f"Get-StartApps JSON error: {error}"
            )
            return []

        except Exception as error:
            print(
                "[ApplicationDiscoveryProvider] "
                f"Windows discovery warning: {error}"
            )
            return []

    # ========================================================
    # SOURCE NORMALIZATION
    # ========================================================

    def _normalize_source_result(
        self,
        result: Any
    ) -> List[Dict[str, Any]]:
        """
        Normalize discovery source output into dictionaries.

        Supported:
            - dict
            - list
            - tuple
            - ApplicationRecord
            - DiscoveryRecord
            - objects exposing to_dict()
            - strings
        """

        if result is None:
            return []

        # ----------------------------------------------------
        # Dictionary container
        # ----------------------------------------------------

        if isinstance(result, dict):

            if "applications" in result:
                result = result["applications"]

            elif "results" in result:
                result = result["results"]

            elif "items" in result:
                result = result["items"]

            else:
                result = [result]

        # ----------------------------------------------------
        # Tuple / list
        # ----------------------------------------------------

        if not isinstance(result, (list, tuple)):
            result = [result]

        output: List[Dict[str, Any]] = []

        # ----------------------------------------------------
        # Individual items
        # ----------------------------------------------------

        for item in result:

            # ------------------------------------------------
            # Object with to_dict()
            # ------------------------------------------------

            if hasattr(item, "to_dict"):

                try:
                    item = item.to_dict()

                except Exception:
                    continue

            # ------------------------------------------------
            # Dictionary
            # ------------------------------------------------

            if isinstance(item, dict):

                name = (
                    item.get("name")
                    or item.get("Name")
                    or item.get("display_name")
                    or item.get("DisplayName")
                    or item.get("title")
                )

                name = self._clean_name(name)

                if not name:
                    continue

                app_id = (
                    item.get("app_id")
                    or item.get("AppID")
                    or item.get("appid")
                )

                executable = (
                    item.get("executable")
                    or item.get("Executable")
                )

                launch_target = (
                    item.get("launch_target")
                    or item.get("LaunchTarget")
                )

                publisher = (
                    item.get("publisher")
                    or item.get("Publisher")
                )

                version = (
                    item.get("version")
                    or item.get("Version")
                )

                install_location = (
                    item.get("install_location")
                    or item.get("InstallLocation")
                )

                output.append(
                    {
                        "name": name,
                        "app_id": app_id,
                        "source": item.get(
                            "source",
                            item.get(
                                "Source",
                                "application_registry"
                            )
                        ),
                        "executable": executable,
                        "launch_target": launch_target,
                        "publisher": publisher,
                        "version": version,
                        "install_location": install_location,
                    }
                )

                continue

            # ------------------------------------------------
            # String
            # ------------------------------------------------

            if isinstance(item, str):

                name = self._clean_name(item)

                if name:
                    output.append(
                        {
                            "name": name,
                            "app_id": None,
                            "source": "application_registry",
                        }
                    )

                continue

        return output

    # ========================================================
    # DISCOVERY RECORD CONVERSION
    # ========================================================

    def _to_record(
        self,
        item: Any,
        default_source: str = "start_apps"
    ) -> DiscoveryRecord | None:
        """
        Convert one application dictionary/object into
        a real DiscoveryRecord.
        """

        # ----------------------------------------------------
        # Already a DiscoveryRecord
        # ----------------------------------------------------

        if isinstance(item, DiscoveryRecord):
            return item

        # ----------------------------------------------------
        # Object -> dictionary
        # ----------------------------------------------------

        if hasattr(item, "to_dict"):

            try:
                item = item.to_dict()

            except Exception:
                return None

        # ----------------------------------------------------
        # Dictionary validation
        # ----------------------------------------------------

        if not isinstance(item, dict):
            return None

        name = (
            item.get("name")
            or item.get("Name")
            or item.get("display_name")
            or item.get("DisplayName")
        )

        name = self._clean_name(name)

        if not name:
            return None

        source = (
            item.get("source")
            or item.get("Source")
            or default_source
        )

        app_id = (
            item.get("app_id")
            or item.get("AppID")
            or item.get("appid")
        )

        executable = (
            item.get("executable")
            or item.get("Executable")
        )

        launch_target = (
            item.get("launch_target")
            or item.get("LaunchTarget")
        )

        publisher = (
            item.get("publisher")
            or item.get("Publisher")
        )

        version = (
            item.get("version")
            or item.get("Version")
        )

        install_location = (
            item.get("install_location")
            or item.get("InstallLocation")
        )

        # ----------------------------------------------------
        # Build normalized metadata
        # ----------------------------------------------------

        metadata = {
            "app_id": app_id,
        }

        if publisher:
            metadata["publisher"] = publisher

        if version:
            metadata["version"] = version

        if install_location:
            metadata["install_location"] = install_location

        # ----------------------------------------------------
        # Create DiscoveryRecord
        # ----------------------------------------------------

        try:

            record = DiscoveryRecord(
                name=name,
                item_type="application",
                source=source,
                location=install_location,
                target=launch_target,
                executable=executable,
                capabilities=[
                    "open",
                    "launch",
                    "search",
                ],
                metadata=metadata,
                launchable=True,
            )

            return record

        except Exception as error:

            print(
                "[ApplicationDiscoveryProvider] "
                f"Record conversion warning for '{name}': {error}"
            )

            return None

    # ========================================================
    # FULL DISCOVERY
    # ========================================================

    def discover(self) -> List[DiscoveryRecord]:
        """
        Discover applications from all currently available
        application sources.

        Registry is used first.
        Windows StartApps fills the inventory when registry
        data is absent or incomplete.
        """

        discovered: List[DiscoveryRecord] = []

        # ----------------------------------------------------
        # Registry source
        # ----------------------------------------------------

        registry_items = self._discover_from_registry()

        for item in registry_items:

            record = self._to_record(
                item,
                default_source="application_registry"
            )

            if record is not None:
                discovered.append(record)

        # ----------------------------------------------------
        # Windows source
        # ----------------------------------------------------

        windows_items = self._discover_from_windows()

        for item in windows_items:

            record = self._to_record(
                item,
                default_source="start_apps"
            )

            if record is not None:
                discovered.append(record)

        # ----------------------------------------------------
        # Deduplicate
        # ----------------------------------------------------

        unique: Dict[str, DiscoveryRecord] = {}

        for record in discovered:

            key = (
                getattr(record, "normalized_name", None)
                or self._clean_name(
                    getattr(record, "name", "")
                ).lower()
            )

            if not key:
                continue

            if key not in unique:
                unique[key] = record

        self.records = list(unique.values())

        return self.records

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, query: str) -> List[DiscoveryRecord]:

        query = self._clean_name(query).lower()

        if not query:
            return []

        results = []

        for record in self.records:

            name = (
                getattr(record, "normalized_name", "")
                or getattr(record, "name", "")
            )

            if query in str(name).lower():
                results.append(record)

        return results

    # ========================================================
    # STATUS
    # ========================================================

    def status(self) -> Dict[str, Any]:

        return {
            "provider": "applications",
            "ready": self.ready,
            "record_count": len(self.records),
        }

    # ========================================================
    # TESTS
    # ========================================================

    def run_tests(self) -> bool:

        print("=" * 65)
        print(
            "    MYX STEP 11.1 APPLICATION DISCOVERY PROVIDER TEST"
        )
        print("=" * 65)

        passed = 0
        total = 5

        # ----------------------------------------------------
        # TEST 1
        # ----------------------------------------------------

        print("\n[TEST 1] Provider Initialization")

        if self.registry is not None and self.ready:
            print("Registry connected: PASS")
            passed += 1
        else:
            print("Registry connected: FAIL")

        # ----------------------------------------------------
        # TEST 2
        # ----------------------------------------------------

        print("\n[TEST 2] Real Application Discovery")

        records = self.discover()

        print(
            f"Applications discovered: {len(records)}"
        )

        if len(records) > 0:
            print("DISCOVERY TEST: PASS")
            passed += 1
        else:
            print("DISCOVERY TEST: FAIL")

        # ----------------------------------------------------
        # TEST 3
        # ----------------------------------------------------

        print("\n[TEST 3] Discovery Record Conversion")

        valid_records = [
            record
            for record in records
            if isinstance(record, DiscoveryRecord)
            and getattr(record, "item_type", None)
            == "application"
        ]

        print(
            f"Valid DiscoveryRecords: {len(valid_records)}"
        )

        if (
            len(valid_records) > 0
            and len(valid_records) == len(records)
        ):
            print("RECORD CONVERSION TEST: PASS")
            passed += 1
        else:
            print("RECORD CONVERSION TEST: FAIL")

        # ----------------------------------------------------
        # TEST 4
        # ----------------------------------------------------

        print("\n[TEST 4] Application Names")

        sample = [
            record.name
            for record in records[:10]
            if getattr(record, "name", None)
        ]

        print(f"Sample applications: {sample}")

        if sample:
            print("NAME TEST: PASS")
            passed += 1
        else:
            print("NAME TEST: FAIL")

        # ----------------------------------------------------
        # TEST 5
        # ----------------------------------------------------

        print("\n[TEST 5] Provider Status")

        status = self.status()

        print(f"Status: {status}")

        if (
            status["ready"]
            and status["record_count"] == len(records)
            and status["record_count"] > 0
        ):
            print("STATUS TEST: PASS")
            passed += 1
        else:
            print("STATUS TEST: FAIL")

        # ----------------------------------------------------
        # FINAL
        # ----------------------------------------------------

        print("\n" + "-" * 65)
        print(f"Tests passed : {passed}/{total}")

        if passed == total:
            print(
                "APPLICATION DISCOVERY PROVIDER TEST: PASS"
            )
            print("STEP 11.1 TEST PASSED")
        else:
            print(
                "APPLICATION DISCOVERY PROVIDER TEST: FAIL"
            )
            print("STEP 11.1 TEST FAILED")

        print("-" * 65)

        return passed == total


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    provider = ApplicationDiscoveryProvider()

    provider.run_tests()
    
