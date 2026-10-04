"""
=========================================
CHITT - Shutdown Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class Shutdown:

    def __init__(self):

        self.modules = [

            "Voice",

            "Vision",

            "Memory",

            "Brain",

            "Plugins",

            "GUI",

            "Engine"

        ]

    # ---------------------------------
    # Save Memory
    # ---------------------------------

    def save_memory(self):

        print("Saving Memory...")

        return True

    # ---------------------------------
    # Stop Voice
    # ---------------------------------

    def stop_voice(self):

        print("Stopping Voice Engine...")

        return True

    # ---------------------------------
    # Stop Vision
    # ---------------------------------

    def stop_vision(self):

        print("Stopping Vision Engine...")

        return True

    # ---------------------------------
    # Stop Plugins
    # ---------------------------------

    def stop_plugins(self):

        print("Stopping Plugins...")

        return True

    # ---------------------------------
    # Close GUI
    # ---------------------------------

    def close_gui(self):

        print("Closing GUI...")

        return True

    # ---------------------------------
    # Shutdown Engine
    # ---------------------------------

    def stop_engine(self):

        print("Stopping Core Engine...")

        return True

    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def shutdown(self):

        print("\n========== SHUTDOWN ==========\n")

        self.save_memory()

        self.stop_voice()

        self.stop_vision()

        self.stop_plugins()

        self.close_gui()

        self.stop_engine()

        print("\nCHITT Shutdown Successfully.")

        return True

    # ---------------------------------
    # Force Shutdown
    # ---------------------------------

    def force_shutdown(self):

        print("Force Shutdown Activated.")

        return True


if __name__ == "__main__":

    shutdown = Shutdown()

    shutdown.shutdown()
    
