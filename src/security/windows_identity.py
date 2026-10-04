"""Windows current-user identity and DPAPI protected bindings."""

from __future__ import annotations

import base64
import ctypes
import json
import sys
from ctypes import wintypes
from typing import Any, Mapping


class WindowsIdentityError(RuntimeError):
    """Raised when Windows identity cannot be verified safely."""


class _DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte))]


def _windows_api():
    if sys.platform != "win32":
        raise WindowsIdentityError("Windows identity APIs are unavailable on this platform.")
    return (
        ctypes.WinDLL("kernel32", use_last_error=True),
        ctypes.WinDLL("advapi32", use_last_error=True),
        ctypes.WinDLL("crypt32", use_last_error=True),
    )


def _blob(data: bytes):
    buffer = ctypes.create_string_buffer(data, len(data))
    value = _DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    return value, buffer


def _last_error(message: str) -> WindowsIdentityError:
    error = ctypes.get_last_error()
    return WindowsIdentityError(f"{message} (Windows error {error}).")


def get_current_windows_sid() -> str:
    """Return the SID from this process's authenticated Windows access token."""
    kernel32, advapi32, _ = _windows_api()
    token = wintypes.HANDLE()
    TOKEN_QUERY = 0x0008
    TokenUser = 1

    advapi32.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
    advapi32.OpenProcessToken.restype = wintypes.BOOL
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    advapi32.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    advapi32.GetTokenInformation.restype = wintypes.BOOL
    advapi32.ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, ctypes.POINTER(wintypes.LPWSTR)]
    advapi32.ConvertSidToStringSidW.restype = wintypes.BOOL
    kernel32.LocalFree.argtypes = [wintypes.HLOCAL]
    kernel32.LocalFree.restype = wintypes.HLOCAL

    if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), TOKEN_QUERY, ctypes.byref(token)):
        raise _last_error("Could not open the current Windows access token")

    try:
        needed = wintypes.DWORD(0)
        advapi32.GetTokenInformation(token, TokenUser, None, 0, ctypes.byref(needed))
        if not needed.value:
            raise _last_error("Could not read the current Windows user identity")
        buffer = ctypes.create_string_buffer(needed.value)
        if not advapi32.GetTokenInformation(token, TokenUser, buffer, needed, ctypes.byref(needed)):
            raise _last_error("Could not read the current Windows user identity")

        # TOKEN_USER begins with a SID_AND_ATTRIBUTES structure; its first field is the SID pointer.
        sid_pointer = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_void_p))[0]
        sid_text = wintypes.LPWSTR()
        if not advapi32.ConvertSidToStringSidW(sid_pointer, ctypes.byref(sid_text)):
            raise _last_error("Could not convert the Windows identity to a SID")
        try:
            result = sid_text.value
        finally:
            kernel32.LocalFree(ctypes.cast(sid_text, wintypes.HLOCAL))
        if not result or not result.startswith("S-"):
            raise WindowsIdentityError("Windows returned an invalid user SID.")
        return result
    finally:
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL
        kernel32.CloseHandle(token)


def _crypt(data: bytes, *, decrypt: bool) -> bytes:
    kernel32, _, crypt32 = _windows_api()
    source, source_buffer = _blob(data)
    entropy, entropy_buffer = _blob(b"MyX.WindowsBinding.v1")
    output = _DATA_BLOB()
    flags = 0x1  # CRYPTPROTECT_UI_FORBIDDEN

    function = crypt32.CryptUnprotectData if decrypt else crypt32.CryptProtectData
    if decrypt:
        function.argtypes = [ctypes.POINTER(_DATA_BLOB), ctypes.POINTER(wintypes.LPWSTR), ctypes.POINTER(_DATA_BLOB), wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(_DATA_BLOB)]
        function.restype = wintypes.BOOL
        ok = function(ctypes.byref(source), None, ctypes.byref(entropy), None, None, flags, ctypes.byref(output))
    else:
        function.argtypes = [ctypes.POINTER(_DATA_BLOB), wintypes.LPCWSTR, ctypes.POINTER(_DATA_BLOB), wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(_DATA_BLOB)]
        function.restype = wintypes.BOOL
        ok = function(ctypes.byref(source), "MyX current Windows user binding", ctypes.byref(entropy), None, None, flags, ctypes.byref(output))

    # Keep the backing buffers alive through the API call.
    _ = source_buffer, entropy_buffer
    if not ok:
        raise _last_error("Windows could not protect or verify the MyX identity binding")
    try:
        return ctypes.string_at(output.pbData, output.cbData)
    finally:
        kernel32.LocalFree(ctypes.cast(output.pbData, wintypes.HLOCAL))


def protect_binding(binding: Mapping[str, Any]) -> str:
    """DPAPI-protect a JSON-serializable binding for the current Windows user."""
    if not isinstance(binding, Mapping):
        raise WindowsIdentityError("Binding data is invalid.")
    try:
        payload = json.dumps(dict(binding), sort_keys=True, separators=(",", ":")).encode("utf-8")
        return base64.b64encode(_crypt(payload, decrypt=False)).decode("ascii")
    except WindowsIdentityError:
        raise
    except Exception as exc:
        raise WindowsIdentityError("Binding data could not be protected.") from exc


def unprotect_binding(protected_binding: str) -> dict[str, Any]:
    """Unprotect and parse a DPAPI binding; malformed data fails closed."""
    try:
        if not isinstance(protected_binding, str) or not protected_binding:
            raise ValueError("empty binding")
        encoded = base64.b64decode(protected_binding.encode("ascii"), validate=True)
        result = json.loads(_crypt(encoded, decrypt=True).decode("utf-8"))
        if not isinstance(result, dict):
            raise ValueError("invalid binding payload")
        return result
    except WindowsIdentityError:
        raise
    except Exception as exc:
        raise WindowsIdentityError("The stored Windows binding is invalid.") from exc


def verify_binding(
    protected_binding: str,
    *,
    expected_sid: str | None = None,
    expected_username: str | None = None,
    expected_account_id: str | None = None,
) -> bool:
    """Verify DPAPI access and that protected identity fields match this user/account."""
    try:
        sid = expected_sid if expected_sid is not None else get_current_windows_sid()
        payload = unprotect_binding(protected_binding)
        if payload.get("version") != 1 or payload.get("sid") != sid:
            return False
        if expected_username is not None and payload.get("username_key") != expected_username.casefold():
            return False
        if expected_account_id is not None and payload.get("account_id") != expected_account_id:
            return False
        return True
    except Exception:
        return False
