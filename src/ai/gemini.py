# -*- coding: utf-8 -*-

"""
CHITT / MYX AI
Gemini Client
"""

from google import genai


class GeminiClient:

    def __init__(self, api_key: str):

        if not api_key:
            raise ValueError(
                "Gemini API key is not configured"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model_name = "gemini-2.5-flash"

        print("[GeminiClient] Initialized")

    def generate(self, prompt: str) -> str:

        prompt = str(prompt).strip()

        if not prompt:
            return ""

        try:

            chat = self.client.chats.create(
                model=self.model_name
            )

            response = chat.send_message(
                prompt
            )

            text = getattr(
                response,
                "text",
                None
            )

            if text is None:
                return ""

            return str(text).strip()

        except UnicodeEncodeError as e:

            print(
                "[GeminiClient] Encoding error:",
                repr(e)
            )

            return ""

        except Exception as e:

            print(
                "[GeminiClient] Generation error:",
                repr(e)
            )

            return ""

    def close(self):

        try:
            self.client = None
        except Exception:
            pass


if __name__ == "__main__":

    print("=" * 60)
    print("GEMINI CLIENT TEST")
    print("=" * 60)

    import os

    api_key = (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
    )

    if not api_key:

        print("GEMINI CLIENT : NOT CONFIGURED")

    else:

        client = GeminiClient(api_key)

        result = client.generate(
            "Reply with exactly: Gemini connection working."
        )

        print("RESULT:", result)

        if result == "":

            print("GEMINI CLIENT : FAIL")

        else:

            print("GEMINI CLIENT : PASS")

        client.close()

    print("=" * 60)
