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

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
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
                e
            )

            return "Gemini response encoding error."

        except Exception as e:

            print(
                "[GeminiClient] Generation error:",
                e
            )

            return f"Gemini Error: {e}"

    def close(self):

        try:
            self.client = None

        except Exception as e:

            print(
                "[GeminiClient] Close warning:",
                e
            )


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("          GEMINI CLIENT TEST")
    print("=" * 60)

    try:

        import os

        api_key = (
            os.getenv("GOOGLE_API_KEY")
            or os.getenv("GEMINI_API_KEY")
        )

        if not api_key:

            print(
                "GEMINI CLIENT : NOT CONFIGURED"
            )

        else:

            client = GeminiClient(api_key)

            result = client.generate(
                "Reply with exactly: Gemini connection working."
            )

            print()
            print("RESULT:", result)

            if result:
                print("GEMINI CLIENT : PASS")
            else:
                print("GEMINI CLIENT : FAIL")

            client.close()

    except Exception as e:

        print()
        print("GEMINI CLIENT : FAIL")
        print("ERROR:", e)

    print("=" * 60)
    