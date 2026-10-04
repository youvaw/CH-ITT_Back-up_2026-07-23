# -*- coding: utf-8 -*-

"""
============================================================
CHITT / MYX AI MANAGER
============================================================

Brain
  ↓
AIManager
  ↓
ProviderManager
  ↓
AI Providers

AIManager चे काम:
    - Brain कडून prompt घेणे
    - ProviderManager ला request देणे
    - AI response परत Brain ला देणे
    - provider बदल Brain पासून लपवणे

Brain मध्ये provider/model-specific code नसावे.
============================================================
"""

from .provider_manager import ProviderManager


class AIManager:
    """
    Stable AI interface used by the Core Brain.

    Brain should communicate only with this class.
    """

    def __init__(self):
        self.provider_manager = ProviderManager()

        print("[AIManager] Provider Manager Connected")

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):
        """
        Return complete AI provider status.
        """
        return self.provider_manager.status()

    # ========================================================
    # AVAILABLE PROVIDERS
    # ========================================================

    def available_providers(self):
        """
        Return currently configured providers.
        """
        return self.provider_manager.available_providers()

    # ========================================================
    # GET PROVIDER
    # ========================================================

    def get_provider(self, name):
        """
        Get a specific provider.
        """
        return self.provider_manager.get_provider(name)

    # ========================================================
    # GENERATE
    # ========================================================

    def generate(self, prompt, provider=None):
        """
        Generate an AI response.

        If provider is not specified,
        ProviderManager automatically selects one.
        """

        prompt = str(prompt).strip()

        if not prompt:
            return ""

        if provider:
            return self.provider_manager.generate(
                prompt,
                provider=provider
            )

        return self.provider_manager.auto_generate(
            prompt
        )

    # ========================================================
    # AUTO GENERATE
    # ========================================================

    def auto_generate(self, prompt):
        """
        Automatically use the configured provider.
        """
        prompt = str(prompt).strip()

        if not prompt:
            return ""

        return self.provider_manager.auto_generate(
            prompt
        )

    # ========================================================
    # READY
    # ========================================================

    def is_ready(self):
        """
        AIManager object is ready if ProviderManager exists.
        """

        return self.provider_manager is not None

    # ========================================================
    # AI AVAILABLE
    # ========================================================

    def has_provider(self):
        """
        Return True when at least one AI provider
        is configured and available.
        """

        providers = self.available_providers()

        return bool(providers)

    # ========================================================
    # SAFE RESPONSE
    # ========================================================

    def ask(self, prompt):
        """
        Main simple interface for Brain.

        Brain can simply call:

            ai_manager.ask(prompt)
        """

        try:

            response = self.auto_generate(prompt)

            if response is None:
                return ""

            return str(response).strip()

        except Exception as e:

            print(
                f"[AIManager] Generation error: {e}"
            )

            return ""

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):
        """
        Close provider resources if providers support close().
        """

        try:

            providers = self.provider_manager.providers

            for provider in providers.values():

                close_method = getattr(
                    provider,
                    "close",
                    None
                )

                if callable(close_method):

                    try:
                        close_method()

                    except Exception as e:
                        print(
                            "[AIManager] Provider close "
                            f"warning: {e}"
                        )

        except Exception as e:

            print(
                f"[AIManager] Close warning: {e}"
            )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("        MYX AI MANAGER TEST")
    print("=" * 60)

    try:

        manager = AIManager()

        print()
        print("AI MANAGER : PASS")
        print(
            "STATUS     :",
            manager.status()
        )
        print(
            "PROVIDERS  :",
            manager.available_providers()
        )
        print(
            "READY      :",
            manager.is_ready()
        )
        print(
            "AI AVAILABLE:",
            manager.has_provider()
        )

        print("=" * 60)

    except Exception as e:

        print()
        print("AI MANAGER : FAIL")
        print("ERROR:", e)
        print("=" * 60)
        