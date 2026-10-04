"""
=========================================
CHITT - Browser Plugin
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import webbrowser

from plugins.plugin_base import PluginBase


class BrowserPlugin(PluginBase):

    def __init__(self):

        super().__init__()

        self.name = "BrowserPlugin"

        self.version = "1.0.0"

        self.description = "Web Browser Control Plugin"

    # ---------------------------------
    # Startup
    # ---------------------------------

    def start(self):

        print(f"{self.name} Started")

    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def stop(self):

        print(f"{self.name} Stopped")

    # ---------------------------------
    # Open URL
    # ---------------------------------

    def open(self, url):

        try:

            webbrowser.open(url)

            return {

                "success": True,

                "url": url

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Google Search
    # ---------------------------------

    def search(self, query):

        url = (

            "https://www.google.com/search?q="

            + query.replace(" ", "+")

        )

        return self.open(url)

    # ---------------------------------
    # YouTube Search
    # ---------------------------------

    def youtube(self, query):

        url = (

            "https://www.youtube.com/results?search_query="

            + query.replace(" ", "+")

        )

        return self.open(url)

    # ---------------------------------
    # Open Google
    # ---------------------------------

    def google(self):

        return self.open(

            "https://www.google.com"

        )

    # ---------------------------------
    # Open YouTube
    # ---------------------------------

    def youtube_home(self):

        return self.open(

            "https://www.youtube.com"

        )

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(

        self,

        command,

        value=None

    ):

        command = command.lower()

        if command == "google":

            return self.google()

        elif command == "youtube":

            return self.youtube_home()

        elif command == "search":

            return self.search(value)

        elif command == "youtube_search":

            return self.youtube(value)

        elif command == "url":

            return self.open(value)

        return {

            "success": False,

            "message": "Unknown command"

        }

    # ---------------------------------
    # Settings
    # ---------------------------------

    def settings(self):

        return {

            "default_browser": "system"

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "plugin": self.name,

            "enabled": self.enabled,

            "status": "OK"

        }


if __name__ == "__main__":

    browser = BrowserPlugin()

    browser.start()

    browser.execute("google")

    browser.execute(

        "search",

        "CHITT AI"

    )

    browser.stop()
    
