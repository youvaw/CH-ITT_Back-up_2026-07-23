"""
=========================================
CHITT - AI Settings
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from settings.settingsmanager import SettingsManager


class AISettings:

    def __init__(self):

        self.settings = SettingsManager()

    # --------------------------
    # AI Model
    # --------------------------

    def get_model(self):

        return self.settings.get("ai_model")

    def set_model(self, model):

        self.settings.set("ai_model", model)

    # --------------------------
    # Memory
    # --------------------------

    def memory_enabled(self):

        return self.settings.get("memory")

    def enable_memory(self):

        self.settings.set("memory", True)

    def disable_memory(self):

        self.settings.set("memory", False)

    # --------------------------
    # Conversation Mode
    # --------------------------

    def conversation_enabled(self):

        return self.settings.get("conversation_mode")

    def enable_conversation(self):

        self.settings.set("conversation_mode", True)

    def disable_conversation(self):

        self.settings.set("conversation_mode", False)

    # --------------------------
    # AI Status
    # --------------------------

    def is_ready(self):

        return True

    # --------------------------
    # Reset AI Settings
    # --------------------------

    def reset(self):

        self.set_model("default")
        self.enable_memory()
        self.enable_conversation()

    # --------------------------
    # Show AI Settings
    # --------------------------

    def show(self):

        print("AI Model          :", self.get_model())
        print("Memory Enabled    :", self.memory_enabled())
        print("Conversation Mode :", self.conversation_enabled())


if __name__ == "__main__":

    ai = AISettings()

    ai.show()

