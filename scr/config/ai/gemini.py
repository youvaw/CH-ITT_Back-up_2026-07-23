"""
CHITT AI
Gemini Client
"""

import google.generativeai as genai


class GeminiClient:

    def __init__(self, api_key: str):

        self.api_key = api_key

        genai.configure(api_key=self.api_key) # type: ignore

        self.model = genai.GenerativeModel("gemini-2.5-flash") # pyright: ignore[reportPrivateImportUsage]

    def ask(self, prompt: str) -> str:

        try:

            response = self.model.generate_content(prompt)

            return response.text

        except Exception as error:

            return f"Gemini Error : {error}"
        