# -*- coding: utf-8 -*-

"""
MyX Input Understanding
-----------------------

Purpose:
    Decide whether user input should enter the
    Global Action Pipeline or remain conversational.

This layer does NOT:
    - discover applications
    - launch applications
    - execute commands
    - contain app-specific names

It only identifies the structural intent of the input.
"""


class InputUnderstanding:
    """
    Lightweight deterministic boundary between
    conversation and system actions.
    """

    ACTION_VERBS = {
        "open",
        "launch",
        "start",
        "run",
        "close",
        "exit",
        "quit",
        "stop",
        "find",
        "locate",
        "search",
        "show",
        "go",
        "visit",
        "play",
        "delete",
        "remove",
        "create",
        "move",
        "copy",
        "rename",
    }

    POLITE_PREFIXES = {
        "please",
        "can you",
        "could you",
        "would you",
        "will you",
    }

    def __init__(self):
        print("[InputUnderstanding] Initialized")

    def normalize(self, text: str) -> str:
        return " ".join(str(text).lower().strip().split())

    def is_action(self, text: str) -> bool:
        text = self.normalize(text)

        if not text:
            return False

        # Direct action:
        # "open chrome"
        first_word = text.split(" ", 1)[0]

        if first_word in self.ACTION_VERBS:
            return True

        # Polite action:
        # "please open chrome"
        # "can you open chrome"
        for prefix in self.POLITE_PREFIXES:
            if text.startswith(prefix + " "):
                remaining = text[len(prefix):].strip()

                if not remaining:
                    return False

                next_word = remaining.split(" ", 1)[0]

                if next_word in self.ACTION_VERBS:
                    return True

        return False

    def classify(self, text: str) -> str:
        """
        Returns:
            "action"
            "conversation"
        """

        if self.is_action(text):
            return "action"

        return "conversation"

    def analyze(self, text: str) -> dict:
        normalized = self.normalize(text)
        intent_type = self.classify(normalized)

        return {
            "text": normalized,
            "type": intent_type,
            "is_action": intent_type == "action",
            "is_conversation": intent_type == "conversation",
        }
    