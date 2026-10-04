"""Optional email recovery provider contract. No provider is configured by default."""

from __future__ import annotations

from abc import ABC, abstractmethod


class EmailRecoveryProvider(ABC):
    """Provider adapters must verify mailbox control and support expiring one-time codes."""

    @abstractmethod
    def is_configured(self) -> bool:
        """Return true only when provider settings and credentials are usable."""
        raise NotImplementedError

    @abstractmethod
    def send_recovery_code(self, address: str, code: str) -> None:
        """Deliver a short-lived code; callers must never log the code."""
        raise NotImplementedError

    @abstractmethod
    def verify_recovery_code(self, address: str, code: str) -> bool:
        """Validate an expiring, single-use code with rate limiting."""
        raise NotImplementedError


_provider: EmailRecoveryProvider | None = None


def configure_email_recovery_provider(provider: EmailRecoveryProvider | None) -> None:
    """Inject an explicitly configured provider adapter; None disables email recovery."""
    global _provider
    if provider is not None and not isinstance(provider, EmailRecoveryProvider):
        raise TypeError("Email recovery provider must implement EmailRecoveryProvider.")
    _provider = provider if provider is not None and provider.is_configured() else None


def get_email_recovery_provider() -> EmailRecoveryProvider | None:
    return _provider


def email_recovery_status() -> str:
    provider = get_email_recovery_provider()
    if provider is None:
        return "Email recovery is not configured. Use your MyX recovery key."
    return "Email recovery provider is configured."
