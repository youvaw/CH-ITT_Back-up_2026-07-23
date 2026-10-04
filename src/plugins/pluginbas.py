"""
CHITT Plugin Base Class
"""


class Plugin:

    def __init__(self):

        self.name = "Plugin"

        self.version = "1.0"

        self.author = "Unknown"

        self.description = ""

    # ==========================================
    # Plugin Information
    # ==========================================

    def info(self):

        return {

            "name": self.name,

            "version": self.version,

            "author": self.author,

            "description": self.description

        }

    # ==========================================
    # Execute Plugin
    # ==========================================

    def execute(self, *args, **kwargs):

        raise NotImplementedError(

            "Plugin must implement execute()"

        )

    # ==========================================
    # Startup
    # ==========================================

    def startup(self):

        print(f"{self.name} Started")

    # ==========================================
    # Shutdown
    # ==========================================

    def shutdown(self):

        print(f"{self.name} Stopped")


if __name__ == "__main__":

    plugin = Plugin()

    print(plugin.info())
"""
=========================================
CHITT - Plugin Base
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from abc import ABC
from abc import abstractmethod


class PluginBase(ABC):

    def __init__(self):

        self.name = self.__class__.__name__

        self.version = "1.0.0"

        self.author = "AVISHKAR"

        self.description = ""

        self.enabled = True

    # ---------------------------------
    # Plugin Information
    # ---------------------------------

    def info(self):

        return {

            "name": self.name,

            "version": self.version,

            "author": self.author,

            "description": self.description,

            "enabled": self.enabled

        }

    # ---------------------------------
    # Enable Plugin
    # ---------------------------------

    def enable(self):

        self.enabled = True

    # ---------------------------------
    # Disable Plugin
    # ---------------------------------

    def disable(self):

        self.enabled = False

    # ---------------------------------
    # Is Enabled
    # ---------------------------------

    def is_enabled(self):

        return self.enabled

    # ---------------------------------
    # Startup
    # ---------------------------------

    @abstractmethod
    def start(self):

        pass

    # ---------------------------------
    # Shutdown
    # ---------------------------------

    @abstractmethod
    def stop(self):

        pass

    # ---------------------------------
    # Execute
    # ---------------------------------

    @abstractmethod
    def execute(

        self,

        *args,

        **kwargs

    ):

        pass

    # ---------------------------------
    # Settings
    # ---------------------------------

    def settings(self):

        return {}

    # ---------------------------------
    # Health Check
    # ---------------------------------

    def health(self):

        return {

            "plugin": self.name,

            "enabled": self.enabled,

            "status": "OK"

        }

    # ---------------------------------
    # String
    # ---------------------------------

    def __str__(self):

        return (

            f"{self.name}"

            f" v{self.version}"

        )
        
