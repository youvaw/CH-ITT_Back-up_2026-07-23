import webbrowser
import subprocess


class AppLauncher:

    def __init__(self):
        print("[AppLauncher] Initialized")

    # ============================================================
    # WEB / APPLICATIONS
    # ============================================================

    def open_google(self):
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    def open_chrome(self):
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]

        for path in chrome_paths:
            try:
                subprocess.Popen(path)
                return "Opening Google Chrome."
            except FileNotFoundError:
                continue

        return "Google Chrome was not found."

    def open_explorer(self):
        try:
            subprocess.Popen("explorer.exe")
            return "Opening File Explorer."
        except Exception as e:
            return f"Unable to open File Explorer: {e}"

    def open_calculator(self):
        try:
            subprocess.Popen("calc.exe")
            return "Opening Calculator."
        except Exception as e:
            return f"Unable to open Calculator: {e}"

    # ============================================================
    # WINDOWS FOLDERS
    # ============================================================

    def open_downloads(self):
        try:
            subprocess.Popen(
                ["explorer.exe", "shell:Downloads"]
            )
            return "Opening Downloads."
        except Exception as e:
            return f"Unable to open Downloads: {e}"

    def open_documents(self):
        try:
            subprocess.Popen(
                ["explorer.exe", "shell:Personal"]
            )
            return "Opening Documents."
        except Exception as e:
            return f"Unable to open Documents: {e}"

    def open_desktop(self):
        try:
            subprocess.Popen(
                ["explorer.exe", "shell:Desktop"]
            )
            return "Opening Desktop."
        except Exception as e:
            return f"Unable to open Desktop: {e}"

    def open_pictures(self):
        try:
            subprocess.Popen(
                ["explorer.exe", "shell:My Pictures"]
            )
            return "Opening Pictures."
        except Exception as e:
            return f"Unable to open Pictures: {e}"

    def open_music(self):
        try:
            subprocess.Popen(
                ["explorer.exe", "shell:My Music"]
            )
            return "Opening Music."
        except Exception as e:
            return f"Unable to open Music: {e}"

    def open_videos(self):
        try:
            subprocess.Popen(
                ["explorer.exe", "shell:My Video"]
            )
            return "Opening Videos."
        except Exception as e:
            return f"Unable to open Videos: {e}"
    def open_settings(self):
        try:
            subprocess.Popen("start ms-settings:", shell=True)
            return "Opening Windows Settings."
        except Exception as e:
            return f"Unable to open Windows Settings: {e}"

    def open_control_panel(self):
        try:
            subprocess.Popen("control.exe")
            return "Opening Control Panel."
        except Exception as e:
            return f"Unable to open Control Panel: {e}"  
    # ============================================================
    # SEARCH
    # ============================================================

    def search_google(self, query):
        query = str(query).strip()

        if not query:
            return "Please tell me what you want to search."

        try:
            import urllib.parse

            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://www.google.com/search?q={encoded_query}"

            webbrowser.open(url)

            return f"Searching Google for {query}."

        except Exception as e:
            return f"Unable to search Google: {e}"

    def search_youtube(self, query):
        query = str(query).strip()

        if not query:
            return "Please tell me what you want to search."

        try:
            import urllib.parse

            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://www.youtube.com/results?search_query={encoded_query}"

            webbrowser.open(url)

            return f"Searching YouTube for {query}."

        except Exception as e:
            return f"Unable to search YouTube: {e}"
    def play_youtube(self, query):
        query = str(query).strip()

        if not query:
            return "Please tell me what you want to play on YouTube."

        try:
            import urllib.parse

            encoded_query = urllib.parse.quote_plus(query)
            url = (
                f"https://www.youtube.com/results"
                f"?search_query={encoded_query}"
            )

            webbrowser.open(url)

            return f"Playing {query} on YouTube."

        except Exception as e:
            return f"Unable to play on YouTube: {e}"
                              
