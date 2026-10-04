import webbrowser


class WebCommands:

    def open_google(self):

        webbrowser.open("https://www.google.com")
        return True

    def open_youtube(self):

        webbrowser.open("https://www.youtube.com")
        return True

    def open_github(self):

        webbrowser.open("https://github.com")
        return True
import webbrowser


class WebCommands:

    def open_google(self):
        webbrowser.open("https://www.google.com")
        return True

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com")
        return True

    def open_github(self):
        webbrowser.open("https://github.com")
        return True

    def open_chatgpt(self):
        webbrowser.open("https://chat.openai.com")
        return True

    def search_google(self, query):

        url = f"https://www.google.com/search?q={query}"

        webbrowser.open(url)

        return True
        
