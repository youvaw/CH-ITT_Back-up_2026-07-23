"""
CHITT AI
Browser Controller
"""

import webbrowser


class Browser:

    def open_google(self):

        webbrowser.open("https://www.google.com")

    def open_youtube(self):

        webbrowser.open("https://www.youtube.com")

    def open_github(self):

        webbrowser.open("https://github.com")

    def search_google(self, query):

        url = f"https://www.google.com/search?q={query}"

        webbrowser.open(url)
        