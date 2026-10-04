"""
CHITT AI
OpenAI Client
"""

import os

from openai import OpenAI


class OpenAIClient:

    def __init__(
        self,
        api_key: str | None = None
    ):

        self.api_key = (
            api_key
            or os.getenv("OPENAI_API_KEY")
        )

        if not self.api_key:

            raise ValueError(
                "OPENAI_API_KEY is not configured"
            )

        self.client = OpenAI(
            api_key=self.api_key
        )

        self.model_name = "gpt-5-mini"

    def generate(self, prompt: str) -> str:

        try:

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": str(prompt)
                    }
                ]
            )

            return (
                response.choices[0]
                .message.content
                or ""
            )

        except Exception as e:

            return f"OpenAI Error: {e}"
        