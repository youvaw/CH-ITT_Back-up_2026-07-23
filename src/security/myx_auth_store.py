"""Versioned, fail-closed local MyX authentication store."""

from __future__ import annotations

import bcrypt
import copy
import json
import os
import re
import tempfile
import uuid
from pathlib import Path
from typing import Any

from . import windows_identity


SCHEMA_VERSION = 1
_BCRYPT_PATTERN = re.compile(r"^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$")


class AuthStoreError(RuntimeError):
    """Raised when MyX authentication data is invalid or cannot be stored safely."""


def find_user_key(users: dict[str, Any], username: str) -> str | None:
    if not isinstance(username, str):
        return None
    folded = username.strip().casefold()
    return next((key for key in users if isinstance(key, str) and key.casefold() == folded), None)


def _valid_bcrypt_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(_BCRYPT_PATTERN.fullmatch(value))


def _validate_data(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise AuthStoreError("MyX authentication store has an unsupported or invalid schema.")
    users = data.get("users")
    if not isinstance(users, dict):
        raise AuthStoreError("MyX authentication store is invalid.")
    folded_names: set[str] = set()
    normalized: dict[str, Any] = {}
    for username, record in users.items():
        if not isinstance(username, str) or not username.strip() or not isinstance(record, dict):
            raise AuthStoreError("MyX authentication store contains an invalid account record.")
        folded = username.casefold()
        if folded in folded_names:
            raise AuthStoreError("MyX authentication store contains duplicate account names.")
        folded_names.add(folded)
        password_hash = record.get("password_hash")
        recovery_hash = record.get("secret_hash", "")
        if not _valid_bcrypt_hash(password_hash) or (recovery_hash and not _valid_bcrypt_hash(recovery_hash)):
            raise AuthStoreError("MyX authentication store contains invalid password or recovery data.")
        account_id = record.get("account_id")
        if not isinstance(account_id, str) or not account_id:
            raise AuthStoreError("MyX authentication store contains an invalid account identity.")
        binding = record.get("windows_binding")
        if binding is not None and (not isinstance(binding, str) or not binding):
            raise AuthStoreError("MyX authentication store contains an invalid Windows binding.")
        email = record.get("recovery_email", "")
        if not isinstance(email, str):
            raise AuthStoreError("MyX authentication store contains invalid recovery contact data.")
        email_verified = record.get("recovery_email_verified", False)
        if not isinstance(email_verified, bool):
            raise AuthStoreError("MyX authentication store contains invalid recovery contact state.")
        normalized[username] = {
            "password_hash": password_hash,
            "secret_hash": recovery_hash,
            "account_id": account_id,
            "windows_binding": binding,
            "recovery_email": email,
            "recovery_email_verified": email_verified,
        }
    return {"schema_version": SCHEMA_VERSION, "users": normalized}


class AuthStore:
    """Keep active auth data in LOCALAPPDATA and migrate the legacy project JSON once."""

    def __init__(self, project_root: str | os.PathLike[str] | None = None, store_dir: str | os.PathLike[str] | None = None):
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]
        self.project_root = Path(project_root)
        if store_dir is None:
            local_app_data = os.environ.get("LOCALAPPDATA")
            if not local_app_data:
                raise AuthStoreError("Windows local application storage is unavailable.")
            store_dir = Path(local_app_data) / "MyX"
        self.store_dir = Path(store_dir)
        self.path = self.store_dir / "auth_store.json"
        self.legacy_path = self.project_root / "myx_credentials.json"
        self._initialize()

    def _initialize(self) -> None:
        try:
            self.store_dir.mkdir(parents=True, exist_ok=True)
            if self.path.exists():
                self._read_active()
                return
            if self.legacy_path.exists():
                migrated = self._load_legacy()
                validated = _validate_data(migrated)
                self._write(validated)
                self._read_active()  # validate the persisted file before it becomes active
                return
            self._write({"schema_version": SCHEMA_VERSION, "users": {}})
            self._read_active()
        except AuthStoreError:
            raise
        except Exception as exc:
            raise AuthStoreError("MyX authentication storage could not be initialized.") from exc

    def _load_legacy(self) -> dict[str, Any]:
        try:
            raw = json.loads(self.legacy_path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise AuthStoreError("Legacy MyX authentication data is invalid.")
            if isinstance(raw.get("users"), dict):
                legacy_users = raw["users"]
            elif isinstance(raw.get("username"), str) and "password_hash" in raw:
                legacy_users = {raw["username"]: raw}
            else:
                raise AuthStoreError("Legacy MyX authentication data is invalid.")
            users: dict[str, Any] = {}
            for username, old_record in legacy_users.items():
                if not isinstance(username, str) or not isinstance(old_record, dict):
                    raise AuthStoreError("Legacy MyX authentication data is invalid.")
                record = {
                    "password_hash": old_record.get("password_hash"),
                    "secret_hash": old_record.get("secret_hash", ""),
                    "account_id": old_record.get("account_id") or str(uuid.uuid4()),
                    "windows_binding": None,
                    "recovery_email": old_record.get("recovery_email", ""),
                    "recovery_email_verified": False,
                }
                users[username] = record
            return {"schema_version": SCHEMA_VERSION, "users": users}
        except AuthStoreError:
            raise
        except Exception as exc:
            raise AuthStoreError("Legacy MyX authentication data could not be read.") from exc

    def _read_active(self) -> dict[str, Any]:
        try:
            return _validate_data(json.loads(self.path.read_text(encoding="utf-8")))
        except AuthStoreError:
            raise
        except Exception as exc:
            raise AuthStoreError("MyX authentication store is corrupted or unreadable.") from exc

    def _write(self, data: dict[str, Any]) -> None:
        validated = _validate_data(data)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        handle, temp_name = tempfile.mkstemp(prefix=".auth_store_", suffix=".tmp", dir=str(self.store_dir))
        try:
            with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
                json.dump(validated, stream, indent=2, ensure_ascii=False)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, self.path)
        except Exception:
            try:
                os.unlink(temp_name)
            except OSError:
                pass
            raise

    def load(self) -> dict[str, Any]:
        return self._read_active()

    def save(self, data: dict[str, Any]) -> None:
        try:
            self._write(data)
            self._read_active()
        except AuthStoreError:
            raise
        except Exception as exc:
            raise AuthStoreError("MyX authentication data could not be saved.") from exc


class MyXAuthService:
    """Authentication operations shared by the UI and safe unit tests."""

    def __init__(self, store: AuthStore):
        self.store = store

    @staticmethod
    def find_user_key(users: dict[str, Any], username: str) -> str | None:
        return find_user_key(users, username)

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        if not isinstance(password, str) or not _valid_bcrypt_hash(stored_hash):
            return False
        try:
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
        except Exception:
            return False

    @staticmethod
    def verify_recovery_key(recovery_key: str, stored_hash: str) -> bool:
        return MyXAuthService.verify_password(recovery_key, stored_hash)

    def authenticate_password(self, username: str, password: str) -> str | None:
        data = self.store.load()
        stored = find_user_key(data["users"], username)
        if stored is None or not self.verify_password(password, data["users"][stored]["password_hash"]):
            return None
        return stored

    def verify_recovery_key_for_user(self, username: str, recovery_key: str) -> bool:
        data = self.store.load()
        stored = find_user_key(data["users"], username)
        return bool(stored and self.verify_recovery_key(recovery_key, data["users"][stored].get("secret_hash", "")))

    def create_account(self, username: str, password: str, recovery_key: str, recovery_email: str = "", bind_to_current_windows_user: bool = True) -> None:
        if not username or not username.strip() or not password or not recovery_key:
            raise AuthStoreError("Username, password, and recovery key are required.")
        data = self.store.load()
        users = data["users"]
        if find_user_key(users, username) is not None:
            raise AuthStoreError("Username already exists.")
        account_id = str(uuid.uuid4())
        record = {
            "password_hash": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii"),
            "secret_hash": bcrypt.hashpw(recovery_key.encode("utf-8"), bcrypt.gensalt()).decode("ascii"),
            "account_id": account_id,
            "windows_binding": None,
            "recovery_email": recovery_email.strip(),
            "recovery_email_verified": False,
        }
        if bind_to_current_windows_user:
            sid = windows_identity.get_current_windows_sid()
            self._ensure_sid_available(data["users"], sid)
            record["windows_binding"] = windows_identity.protect_binding({
                "version": 1,
                "sid": sid,
                "username_key": username.strip().casefold(),
                "account_id": account_id,
            })
        users[username.strip()] = record
        self.store.save(data)

    def _ensure_sid_available(self, users: dict[str, Any], sid: str, allowed_username: str | None = None) -> None:
        for existing_username, account in users.items():
            protected = account.get("windows_binding")
            if not protected:
                continue
            if windows_identity.verify_binding(
                protected,
                expected_sid=sid,
                expected_username=existing_username.casefold(),
                expected_account_id=account["account_id"],
            ) and existing_username != allowed_username:
                raise AuthStoreError("This Windows account is already bound to a different MyX account.")

    def setup_windows_binding(self, username: str, *, user_authorized: bool = False) -> None:
        if not user_authorized:
            raise AuthStoreError("Explicit MyX authentication and user confirmation are required to bind this account.")
        data = self.store.load()
        stored = find_user_key(data["users"], username)
        if stored is None:
            raise AuthStoreError("MyX account was not found.")
        account = data["users"][stored]
        sid = windows_identity.get_current_windows_sid()
        self._ensure_sid_available(data["users"], sid, allowed_username=stored)
        protected = windows_identity.protect_binding({
            "version": 1,
            "sid": sid,
            "username_key": stored.casefold(),
            "account_id": account["account_id"],
        })
        account["windows_binding"] = protected
        self.store.save(data)

    def _matching_bound_user(self) -> str | None:
        data = self.store.load()
        matches = []
        for username, account in data["users"].items():
            protected = account.get("windows_binding")
            if protected and windows_identity.verify_binding(
                protected,
                expected_username=username.casefold(),
                expected_account_id=account["account_id"],
            ):
                matches.append(username)
        return matches[0] if len(matches) == 1 else None

    def is_windows_user_bound(self, username: str | None = None) -> bool:
        try:
            matching = self._matching_bound_user()
            return matching is not None and (username is None or matching.casefold() == username.strip().casefold())
        except Exception:
            return False

    def authenticate_current_windows_user(self) -> str | None:
        try:
            return self._matching_bound_user()
        except Exception:
            return None
