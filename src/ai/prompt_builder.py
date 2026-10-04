"""
Prompt Builder
"""


class PromptBuilder:

    def build(self, user_input: str):

        return f"""
You are CHITT AI.

Reply naturally.

User:
{user_input}

Assistant:
"""
    
