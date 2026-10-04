# ============================================================
# MYX GLOBAL ACTION AUDIT
# PRODUCTION CLEAN VERSION
# ============================================================

from __future__ import annotations

from datetime import datetime
import json
import os
from typing import Any


class GlobalActionAudit:
    """
    Production audit layer for MYX actions.

    Responsibilities:
        - Record every action
        - Preserve command
        - Preserve action
        - Preserve decision
        - Preserve target information
        - Preserve success/failure
        - Preserve execution message
        - Never crash the main pipeline
    """

    def __init__(
        self,
        audit_file=None,
        max_records=1000,
    ):

        self.records = []

        self.max_records = int(
            max_records
        )

        if audit_file is None:

            project_root = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../..",
                )
            )

            audit_dir = os.path.join(
                project_root,
                "data",
                "audit",
            )

            os.makedirs(
                audit_dir,
                exist_ok=True,
            )

            audit_file = os.path.join(
                audit_dir,
                "global_actions.jsonl",
            )

        self.audit_file = audit_file

        print("[GlobalActionAudit] Initialized")

    # ========================================================
    # TARGET SERIALIZATION
    # ========================================================

    def serialize_target(
        self,
        target: Any,
    ):

        if target is None:
            return None

        if isinstance(target, str):
            return target

        if isinstance(target, dict):

            result = {}

            for key, value in target.items():

                if key in {
                    "name",
                    "normalized_name",
                    "item_type",
                    "source",
                    "location",
                    "target",
                    "executable",
                    "launchable",
                    "capabilities",
                    "metadata",
                    "app_id",
                    "url",
                    "path",
                    "full_path",
                    "file_path",
                    "launch_target",
                }:

                    try:

                        json.dumps(
                            value
                        )

                        result[key] = value

                    except Exception:

                        result[key] = str(
                            value
                        )

            return result

        # ----------------------------------------------------
        # Generic object / DiscoveryRecord
        # ----------------------------------------------------

        result = {}

        fields = (
            "name",
            "normalized_name",
            "item_type",
            "source",
            "location",
            "target",
            "executable",
            "launchable",
            "capabilities",
            "metadata",
            "app_id",
            "url",
            "path",
            "full_path",
            "file_path",
            "launch_target",
        )

        for field in fields:

            try:

                if hasattr(
                    target,
                    field,
                ):

                    value = getattr(
                        target,
                        field,
                    )

                    try:
                        json.dumps(
                            value
                        )

                        result[field] = value

                    except Exception:

                        result[field] = str(
                            value
                        )

            except Exception:
                continue

        if result:
            return result

        return {
            "type": type(target).__name__,
            "repr": repr(target),
        }

    # ========================================================
    # ADD RECORD
    # ========================================================

    def add_record(
        self,
        record,
    ):

        if not isinstance(
            record,
            dict,
        ):
            record = {
                "message": str(record)
            }

        safe_record = dict(
            record
        )

        safe_record.setdefault(
            "timestamp",
            datetime.now().isoformat(),
        )

        safe_record["target"] = (
            self.serialize_target(
                safe_record.get(
                    "target"
                )
            )
        )

        self.records.append(
            safe_record
        )

        # Keep memory bounded
        if len(self.records) > self.max_records:

            self.records = (
                self.records[
                    -self.max_records:
                ]
            )

        self._write_record(
            safe_record
        )

        return safe_record

    # ========================================================
    # RECORD RESULT API
    # ========================================================

    def record_result(
        self,
        command,
        action,
        decision,
        target,
        success,
        message,
        **extra,
    ):

        record = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "action": action,
            "decision": decision,
            "target": target,
            "success": bool(success),
            "message": message,
        }

        record.update(
            extra
        )

        return self.add_record(
            record
        )

    # ========================================================
    # WRITE JSONL
    # ========================================================

    def _write_record(
        self,
        record,
    ):

        try:

            directory = os.path.dirname(
                self.audit_file
            )

            if directory:
                os.makedirs(
                    directory,
                    exist_ok=True,
                )

            with open(
                self.audit_file,
                "a",
                encoding="utf-8",
            ) as file:

                file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False,
                        default=str,
                    )
                )

                file.write(
                    "\n"
                )

        except Exception as exc:

            # Audit must NEVER break execution.
            print(
                f"[GlobalActionAudit] "
                f"Write warning: {exc}"
            )

    # ========================================================
    # READ MEMORY RECORDS
    # ========================================================

    def get_records(
        self,
        limit=None,
    ):

        if limit is None:
            return list(
                self.records
            )

        try:
            limit = int(
                limit
            )
        except Exception:
            return list(
                self.records
            )

        if limit <= 0:
            return []

        return list(
            self.records[
                -limit:
            ]
        )

    # ========================================================
    # CLEAR MEMORY
    # ========================================================

    def clear_records(self):

        self.records.clear()

    # ========================================================
    # TEST
    # ========================================================

    def run_tests(self):

        print()
        print("=" * 64)
        print("MYX GLOBAL ACTION AUDIT TEST")
        print("PRODUCTION CLEAN VERSION")
        print("=" * 64)

        passed = 0
        total = 4

        # ----------------------------------------------------
        # TEST 1
        # ----------------------------------------------------

        record = self.add_record(
            {
                "command": "open chrome",
                "action": "open",
                "decision": "execute",
                "target": {
                    "name": "Google Chrome",
                    "item_type": "application",
                    "app_id": "Chrome",
                },
                "success": True,
                "message": "Opened Google Chrome",
            }
        )

        if (
            isinstance(record, dict)
            and len(self.records) >= 1
        ):
            print("[1] Record Creation PASS")
            passed += 1
        else:
            print("[1] Record Creation FAIL")

        # ----------------------------------------------------
        # TEST 2
        # ----------------------------------------------------

        target = {
            "name": "Test",
            "item_type": "application",
            "app_id": "Test.App",
        }

        serialized = self.serialize_target(
            target
        )

        if (
            isinstance(serialized, dict)
            and serialized.get("name") == "Test"
        ):
            print("[2] Target Serialization PASS")
            passed += 1
        else:
            print("[2] Target Serialization FAIL")

        # ----------------------------------------------------
        # TEST 3
        # ----------------------------------------------------

        self.record_result(
            command="test",
            action="open",
            decision="execute",
            target=target,
            success=False,
            message="Test failure",
        )

        if len(self.records) >= 2:
            print("[3] Result Recording PASS")
            passed += 1
        else:
            print("[3] Result Recording FAIL")

        # ----------------------------------------------------
        # TEST 4
        # ----------------------------------------------------

        records = self.get_records(
            limit=1
        )

        if (
            isinstance(records, list)
            and len(records) == 1
        ):
            print("[4] Record Retrieval PASS")
            passed += 1
        else:
            print("[4] Record Retrieval FAIL")

        print()
        print("=" * 64)
        print(
            f"Tests passed : "
            f"{passed}/{total}"
        )

        if passed == total:
            print(
                "GLOBAL ACTION AUDIT TEST: PASS"
            )
        else:
            print(
                "GLOBAL ACTION AUDIT TEST: FAIL"
            )

        print("=" * 64)
        print()

        return passed == total


if __name__ == "__main__":

    audit = GlobalActionAudit()

    raise SystemExit(
        0
        if audit.run_tests()
        else 1
    )
