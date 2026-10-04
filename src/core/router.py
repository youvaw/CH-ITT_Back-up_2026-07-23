from src.system.app_launcher import AppLauncher


class CommandRouter:

    def __init__(self):
        self.app_launcher = AppLauncher()
        print("[Router] Command Router Initialized")

    # ============================================================
    # NORMALIZATION
    # ============================================================

    def normalize(self, text):
        return str(text).strip().lower()

    # ============================================================
    # PHRASE MATCHING
    # ============================================================

    def contains_any(self, text, phrases):
        return any(phrase in text for phrase in phrases)

    # ============================================================
    # APPLICATION COMMANDS
    # ============================================================

    def open_google(self):
        return self.app_launcher.open_google()

    def open_youtube(self):
        return self.app_launcher.open_youtube()

    def open_chrome(self):
        return self.app_launcher.open_chrome()

    def open_explorer(self):
        return self.app_launcher.open_explorer()

    def open_calculator(self):
        return self.app_launcher.open_calculator()

    # ============================================================
    # WINDOWS SETTINGS / CONTROL PANEL
    # ============================================================

    def open_settings(self):
        return self.app_launcher.open_settings()

    def open_control_panel(self):
        return self.app_launcher.open_control_panel()

    # ============================================================
    # WINDOWS FOLDERS
    # ============================================================

    def open_downloads(self):
        return self.app_launcher.open_downloads()

    def open_documents(self):
        return self.app_launcher.open_documents()

    def open_desktop(self):
        return self.app_launcher.open_desktop()

    def open_pictures(self):
        return self.app_launcher.open_pictures()

    def open_music(self):
        return self.app_launcher.open_music()

    def open_videos(self):
        return self.app_launcher.open_videos()

    # ============================================================
    # SEARCH COMMANDS
    # ============================================================

    def search_google(self, query):
        return self.app_launcher.search_google(query)

    def search_youtube(self, query):
        return self.app_launcher.search_youtube(query)

    # ============================================================
    # PLAY ON YOUTUBE
    # ============================================================

    def play_youtube(self, query):
        return self.app_launcher.play_youtube(query)

    # ============================================================
    # MAIN COMMAND ROUTER
    # ============================================================

    def execute(self, command):

        command = self.normalize(command)

        print(f"[Router] Command: {command}")

        # ========================================================
        # GOOGLE SEARCH
        # ========================================================

        google_prefixes = [
            "search google for ",
            "search google ",
            "google search for ",
            "google search ",
            "search on google for ",
            "search on google ",
        ]

        for prefix in google_prefixes:

            if command.startswith(prefix):

                query = command[len(prefix):].strip()

                if query:
                    return self.search_google(query)

                return "Please tell me what you want to search on Google."

        # ========================================================
        # YOUTUBE SEARCH
        # ========================================================

        youtube_prefixes = [
            "search youtube for ",
            "search youtube ",
            "youtube search for ",
            "youtube search ",
            "search on youtube for ",
            "search on youtube ",
        ]

        for prefix in youtube_prefixes:

            if command.startswith(prefix):

                query = command[len(prefix):].strip()

                if query:
                    return self.search_youtube(query)

                return "Please tell me what you want to search on YouTube."

        # ========================================================
        # PLAY ON YOUTUBE
        # ========================================================

        youtube_play_prefixes = [
            "play music ",
            "play song ",
            "play ",
        ]

        for prefix in youtube_play_prefixes:

            if command.startswith(prefix):

                query = command[len(prefix):].strip()

                if query.endswith(" on youtube"):
                    query = query[:-10].strip()

                if query:
                    return self.play_youtube(query)

                return "Please tell me what you want to play."

        # ========================================================
        # OPEN GOOGLE
        # ========================================================

        if self.contains_any(command, [
            "open google",
            "google open",
            "launch google",
            "start google",
            "ओपन गूगल",
            "गूगल उघड",
            "गूगल ओपन",
        ]):
            return self.open_google()

        # ========================================================
        # OPEN YOUTUBE
        # ========================================================

        if self.contains_any(command, [
            "open youtube",
            "youtube open",
            "launch youtube",
            "start youtube",
            "ओपन यूट्यूब",
            "ओपन युट्युब",
            "यूट्यूब उघड",
            "युट्युब उघड",
        ]):
            return self.open_youtube()

        # ========================================================
        # OPEN CHROME
        # ========================================================

        if self.contains_any(command, [
            "open chrome",
            "chrome open",
            "launch chrome",
            "start chrome",
            "ओपन क्रोम",
            "क्रोम उघड",
        ]):
            return self.open_chrome()

        # ========================================================
        # FILE EXPLORER
        # ========================================================

        if self.contains_any(command, [
            "open file explorer",
            "open explorer",
            "file explorer",
            "explorer open",
            "launch explorer",
            "start explorer",
            "ओपन फाइल एक्सप्लोरर",
            "फाइल एक्सप्लोरर उघड",
        ]):
            return self.open_explorer()

        # ========================================================
        # CALCULATOR
        # ========================================================

        if self.contains_any(command, [
            "open calculator",
            "calculator open",
            "launch calculator",
            "start calculator",
            "ओपन कॅल्क्युलेटर",
            "कॅल्क्युलेटर उघड",
        ]):
            return self.open_calculator()

        # ========================================================
        # WINDOWS SETTINGS
        # ========================================================

        if self.contains_any(command, [
            "open settings",
            "settings open",
            "launch settings",
            "start settings",
            "windows settings",
            "open windows settings",
            "ओपन सेटिंग्स",
            "सेटिंग्स उघड",
            "विंडोज सेटिंग्स उघड",
        ]):
            return self.open_settings()

        # ========================================================
        # CONTROL PANEL
        # ========================================================

        if self.contains_any(command, [
            "open control panel",
            "control panel open",
            "launch control panel",
            "start control panel",
            "windows control panel",
            "ओपन कंट्रोल पॅनेल",
            "कंट्रोल पॅनेल उघड",
        ]):
            return self.open_control_panel()

        # ========================================================
        # DOWNLOADS
        # ========================================================

        if self.contains_any(command, [
            "open downloads",
            "open download",
            "downloads open",
            "download open",
            "launch downloads",
            "start downloads",
            "ओपन डाउनलोड्स",
            "डाउनलोड्स उघड",
            "डाउनलोड उघड",
        ]):
            return self.open_downloads()

        # ========================================================
        # DOCUMENTS
        # ========================================================

        if self.contains_any(command, [
            "open documents",
            "open document",
            "documents open",
            "document open",
            "launch documents",
            "start documents",
            "ओपन डॉक्युमेंट्स",
            "डॉक्युमेंट्स उघड",
            "डॉक्युमेंट उघड",
        ]):
            return self.open_documents()

        # ========================================================
        # DESKTOP
        # ========================================================

        if self.contains_any(command, [
            "open desktop",
            "desktop open",
            "launch desktop",
            "start desktop",
            "ओपन डेस्कटॉप",
            "डेस्कटॉप उघड",
        ]):
            return self.open_desktop()

        # ========================================================
        # PICTURES
        # ========================================================

        if self.contains_any(command, [
            "open pictures",
            "open picture",
            "pictures open",
            "picture open",
            "launch pictures",
            "start pictures",
            "ओपन पिक्चर्स",
            "पिक्चर्स उघड",
            "फोटो उघड",
        ]):
            return self.open_pictures()

        # ========================================================
        # MUSIC
        # ========================================================

        if self.contains_any(command, [
            "open music",
            "music open",
            "launch music",
            "start music",
            "ओपन म्युझिक",
            "म्युझिक उघड",
            "गाणी उघड",
        ]):
            return self.open_music()

        # ========================================================
        # VIDEOS
        # ========================================================

        if self.contains_any(command, [
            "open videos",
            "open video",
            "videos open",
            "video open",
            "launch videos",
            "start videos",
            "ओपन व्हिडिओ",
            "ओपन व्हिडिओज",
            "व्हिडिओ उघड",
        ]):
            return self.open_videos()

        # ========================================================
        # FALLBACK
        # ========================================================

        return "I don't know that command yet."
    
