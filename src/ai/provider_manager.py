"""
CHITT AI
Central AI Provider Manager
"""

import os

from .deepseek import DeepSeekClient
from .gemini import GeminiClient
from .openai_client import OpenAIClient


class ProviderManager:

    def __init__(self):

        self.providers = {}

        self._load_deepseek()
        self._load_gemini()
        self._load_openai()

    # ------------------------------------------------
    # DeepSeek
    # ------------------------------------------------

    def _load_deepseek(self):

        api_key = os.getenv(
            "DEEPSEEK_API_KEY"
        )

        if not api_key:

            print(
                "[ProviderManager] "
                "DeepSeek: NOT CONFIGURED"
            )

            return

        try:

            self.providers["deepseek"] = (
                DeepSeekClient(api_key)
            )

            print(
                "[ProviderManager] "
                "DeepSeek: READY"
            )

        except Exception as e:

            print(
                "[ProviderManager] "
                f"DeepSeek: ERROR - {e}"
            )

    # ------------------------------------------------
    # Gemini
    # ------------------------------------------------

    def _load_gemini(self):

        api_key = (
            os.getenv("GOOGLE_API_KEY")
            or os.getenv("GEMINI_API_KEY")
        )

        if not api_key:

            print(
                "[ProviderManager] "
                "Gemini: NOT CONFIGURED"
            )

            return

        try:

            self.providers["gemini"] = (
                GeminiClient(api_key)
            )

            print(
                "[ProviderManager] "
                "Gemini: READY"
            )

        except Exception as e:

            print(
                "[ProviderManager] "
                f"Gemini: ERROR - {e}"
            )

    # ------------------------------------------------
    # OpenAI
    # ------------------------------------------------

    def _load_openai(self):

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:

            print(
                "[ProviderManager] "
                "OpenAI: NOT CONFIGURED"
            )

            return

        try:

            self.providers["openai"] = (
                OpenAIClient(api_key)
            )

            print(
                "[ProviderManager] "
                "OpenAI: READY"
            )

        except Exception as e:

            print(
                "[ProviderManager] "
                f"OpenAI: ERROR - {e}"
            )

    # ------------------------------------------------
    # Provider List
    # ------------------------------------------------

    def available_providers(self):

        return list(
            self.providers.keys()
        )

    # ------------------------------------------------
    # Get Provider
    # ------------------------------------------------

    def get_provider(self, name: str):

        name = str(name).strip().lower()

        return self.providers.get(name)

    # ------------------------------------------------
    # Generate
    # ------------------------------------------------

    def generate(
        self,
        prompt: str,
        provider: str = "deepseek"
    ):

        provider = (
            str(provider)
            .strip()
            .lower()
        )

        client = self.get_provider(
            provider
        )

        if client is None:

            return (
                f"AI provider "
                f"'{provider}' "
                f"is not available."
            )

        return client.generate(
            prompt
        )

    # ------------------------------------------------
    # Automatic Provider Selection
    # ------------------------------------------------

    def auto_generate(
        self,
        prompt: str
    ):

        priority = [
            "deepseek",
            "gemini",
            "openai"
        ]

        for provider in priority:

            if provider in self.providers:

                return self.providers[
                    provider
                ].generate(prompt)

        return (
            "No AI provider is configured."
        )

    # ------------------------------------------------
    # Status
    # ------------------------------------------------

    def status(self):

        return {

            "providers":
                self.available_providers(),

            "count":
                len(self.providers)

        }


if __name__ == "__main__":

    manager = ProviderManager()

    print()

    print(
        "AVAILABLE PROVIDERS:"
    )

    print(
        manager.status()
    )
    