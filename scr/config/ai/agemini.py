"""
CHITT AI
Gemini Client
"""

import google.generativeai as genai


class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key) # pyright: ignore[reportPrivateImportUsage]
        self.model = genai.GenerativeModel("gemini-2.5-flash") # pyright: ignore[reportPrivateImportUsage]

    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"Gemini Error: {e}"
        