"""
CHITT Shutdown Manager
"""

from logger.logger import Logger


class Shutdown:

    def __init__(self):

        self.logger = Logger()

    # ==========================================
    # Save Database
    # ==========================================

    def save_database(self, database):

        if database:

            try:

                database.close()

                self.logger.info("Database Closed")

            except Exception as error:

                self.logger.error(f"Database Error : {error}")

    # ==========================================
    # Save Memory
    # ==========================================

    def save_memory(self, brain):

        try:

            if hasattr(brain, "learning"):

                brain.learning.save()

                self.logger.info("Learning Saved")

        except Exception as error:

            self.logger.error(f"Memory Error : {error}")

    # ==========================================
    # Shutdown Voice
    # ==========================================

    def stop_voice(self, voice):

        try:

            if voice and hasattr(voice, "stop"):

                voice.stop()

                self.logger.info("Voice Stopped")

        except Exception as error:

            self.logger.error(f"Voice Error : {error}")

    # ==========================================
    # Shutdown Plugins
    # ==========================================

    def stop_plugins(self, plugins):

        try:

            if plugins:

                for plugin in plugins.plugins.values():

                    plugin.shutdown()

                self.logger.info("Plugins Stopped")

        except Exception as error:

            self.logger.error(f"Plugin Error : {error}")

    # ==========================================
    # Safe Shutdown
    # ==========================================

    def shutdown(

        self,

        database=None,

        brain=None,

        voice=None,

        plugins=None

    ):

        print("\nShutting Down CHITT...\n")

        self.save_memory(brain)

        self.stop_plugins(plugins)

        self.stop_voice(voice)

        self.save_database(database)

        self.logger.info("System Shutdown Complete")

        print("CHITT Shutdown Successfully")


if __name__ == "__main__":

    shutdown = Shutdown()

    shutdown.shutdown()
    
