"""Security-focused tests for local MyX auth. Test data is synthetic; values are never printed."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import bcrypt

from src.security import windows_identity
from src.security.myx_auth_store import AuthStore, AuthStoreError, MyXAuthService


def _hash(value: str) -> str:
    return bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


class MyXAuthSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store_dir = self.root / "local" / "MyX"
        self.project = self.root / "project"
        self.project.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    @unittest.skipUnless(sys.platform == "win32", "Windows token APIs require Windows")
    def test_windows_sid_retrieval(self):
        self.assertRegex(windows_identity.get_current_windows_sid(), r"^S-\d-")

    @unittest.skipUnless(sys.platform == "win32", "DPAPI requires Windows")
    def test_dpapi_protect_unprotect_and_binding(self):
        sid = windows_identity.get_current_windows_sid()
        payload = {"version": 1, "sid": sid, "username_key": "unit-user", "account_id": "test-id"}
        protected = windows_identity.protect_binding(payload)
        self.assertTrue(bool(protected))
        self.assertTrue(windows_identity.unprotect_binding(protected) == payload)
        self.assertTrue(windows_identity.verify_binding(protected, expected_sid=sid, expected_username="unit-user", expected_account_id="test-id"))
        self.assertFalse(windows_identity.verify_binding(protected, expected_sid="S-1-0-0"))
        self.assertFalse(windows_identity.verify_binding("corrupt", expected_sid=sid))

    def test_store_creation_and_case_insensitive_lookup(self):
        store = AuthStore(self.project, self.store_dir)
        service = MyXAuthService(store)
        data = store.load()
        self.assertEqual(data["schema_version"], 1)
        self.assertIsNone(service.find_user_key(data["users"], "unknown"))
        self.assertTrue(store.path.exists())

    def test_existing_account_migration_preserves_hashes_and_validates(self):
        password_hash = _hash("unit password")
        recovery_hash = _hash("unit recovery")
        legacy = {"users": {"MiXeDUser": {"password_hash": password_hash, "secret_hash": recovery_hash}}}
        (self.project / "myx_credentials.json").write_text(json.dumps(legacy), encoding="utf-8")
        backup = self.project / "myx_credentials.backup.json"
        backup.write_text("preserved backup marker", encoding="utf-8")
        backup_before = backup.read_bytes()
        store = AuthStore(self.project, self.store_dir)
        data = store.load()
        migrated = data["users"]["MiXeDUser"]
        self.assertTrue(migrated["password_hash"] == password_hash)
        self.assertTrue(migrated["secret_hash"] == recovery_hash)
        self.assertFalse(bool(migrated["windows_binding"]))
        self.assertTrue((self.project / "myx_credentials.json").exists())
        self.assertTrue(backup.read_bytes() == backup_before)

    def test_legacy_single_account_migration(self):
        legacy = {"username": "LegacyUser", "password_hash": _hash("unit password"), "secret_hash": _hash("unit recovery")}
        (self.project / "myx_credentials.json").write_text(json.dumps(legacy), encoding="utf-8")
        store = AuthStore(self.project, self.store_dir)
        self.assertIn("LegacyUser", store.load()["users"])

    def test_invalid_legacy_migration_does_not_activate_store(self):
        (self.project / "myx_credentials.json").write_text(json.dumps({"users": {"bad": {"password_hash": "invalid"}}}), encoding="utf-8")
        with self.assertRaises(AuthStoreError):
            AuthStore(self.project, self.store_dir)
        self.assertFalse((self.store_dir / "auth_store.json").exists())

    def test_password_recovery_and_case_insensitive_username(self):
        store = AuthStore(self.project, self.store_dir)
        service = MyXAuthService(store)
        with mock.patch("src.security.myx_auth_store.windows_identity.get_current_windows_sid", return_value="S-1-5-21-test"), mock.patch("src.security.myx_auth_store.windows_identity.protect_binding", return_value="test-protected"):
            service.create_account("CaseUser", "unit password", "unit recovery", bind_to_current_windows_user=True)
        data = store.load()
        account = data["users"]["CaseUser"]
        self.assertEqual(service.find_user_key(data["users"], "caseuser"), "CaseUser")
        self.assertEqual(service.authenticate_password(" CASEUSER ", "unit password"), "CaseUser")
        self.assertIsNone(service.authenticate_password("CaseUser", "wrong password"))
        self.assertTrue(service.verify_recovery_key("unit recovery", account["secret_hash"]))
        self.assertFalse(service.verify_recovery_key("wrong recovery", account["secret_hash"]))

    def test_new_account_setup_and_windows_authentication(self):
        store = AuthStore(self.project, self.store_dir)
        service = MyXAuthService(store)
        current_sid = "S-1-5-21-current"
        with mock.patch("src.security.myx_auth_store.windows_identity.get_current_windows_sid", return_value=current_sid), mock.patch("src.security.myx_auth_store.windows_identity.protect_binding", side_effect=lambda payload: json.dumps(payload)), mock.patch("src.security.myx_auth_store.windows_identity.verify_binding", side_effect=lambda blob, **kw: json.loads(blob).get("sid") == current_sid and json.loads(blob).get("username_key") == kw.get("expected_username") and json.loads(blob).get("account_id") == kw.get("expected_account_id")):
            service.create_account("BoundUser", "unit password", "unit recovery")
            self.assertTrue(service.is_windows_user_bound())
            self.assertEqual(service.authenticate_current_windows_user(), "BoundUser")
            with self.assertRaises(AuthStoreError):
                service.setup_windows_binding("BoundUser")
            service.setup_windows_binding("BoundUser", user_authorized=True)
            self.assertEqual(service.authenticate_current_windows_user(), "BoundUser")

    def test_unbound_user_and_corrupted_binding_fail_closed(self):
        store = AuthStore(self.project, self.store_dir)
        service = MyXAuthService(store)
        data = {"schema_version": 1, "users": {"Unbound": {"password_hash": _hash("unit"), "secret_hash": _hash("recovery"), "account_id": "id", "windows_binding": None}}}
        store.save(data)
        self.assertFalse(service.is_windows_user_bound())
        self.assertIsNone(service.authenticate_current_windows_user())
        data["users"]["Unbound"]["windows_binding"] = "corrupt"
        store.save(data)
        with mock.patch("src.security.myx_auth_store.windows_identity.verify_binding", return_value=False):
            self.assertFalse(service.is_windows_user_bound())
            self.assertIsNone(service.authenticate_current_windows_user())

    def test_corrupted_active_store_fails_closed(self):
        store = AuthStore(self.project, self.store_dir)
        store.path.write_text("{broken", encoding="utf-8")
        with self.assertRaises(AuthStoreError):
            store.load()

    def test_email_recovery_is_unconfigured_by_default(self):
        from src.security.email_recovery import email_recovery_status, get_email_recovery_provider
        self.assertIsNone(get_email_recovery_provider())
        self.assertIn("not configured", email_recovery_status())


if __name__ == "__main__":
    unittest.main()

