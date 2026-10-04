import sys
import os
import time
import io
import wave
import sqlite3
import threading
import traceback

import numpy as np
import sounddevice as sd
import speech_recognition as sr
import pyttsx3

from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# WINDOWS UTF-8
# ============================================================

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(
            encoding="utf-8",
            errors="replace"
        )
        sys.stderr.reconfigure(
            encoding="utf-8",
            errors="replace"
        )
    except Exception:
        pass


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.append(BASE_DIR)


# ============================================================
# .ENV
# ============================================================

dotenv_path = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(
    dotenv_path=dotenv_path,
    override=True
)


# ============================================================
# GUI
# ============================================================

try:
    from src.gui.mainwindow import MainWindow
except Exception as e:
    MainWindow = None
    print(f"[MAYAX GUI Warning]: {e}")


# ============================================================
# LOGGING
# ============================================================

LOG_FILE = os.path.join(
    BASE_DIR,
    "mayax_debug.log"
)


def log_msg(text):

    try:

        text = str(text)

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{text}\n"
            )

        print(text)

    except Exception as e:

        print(
            f"[Logging Error]: {repr(e)}"
        )


# ============================================================
# MEMORY
# ============================================================

class MayaxMemory:

    def __init__(
        self,
        db_file="mayax_memory.db"
    ):

        self.db_file = os.path.abspath(
            db_file
        )

        self._init_db()


    def _get_connection(self):

        conn = sqlite3.connect(
            self.db_file
        )

        conn.row_factory = sqlite3.Row

        return conn


    def _init_db(self):

        try:

            with self._get_connection() as conn:

                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        user_input TEXT NOT NULL,
                        mayax_response TEXT NOT NULL
                    )
                """)

                conn.commit()

        except Exception as e:

            log_msg(
                f"Memory Init Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )


    def save_turn(
        self,
        user_input,
        bot_response
    ):

        try:

            now = datetime.now().isoformat()

            with self._get_connection() as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO chat_history
                    (
                        timestamp,
                        user_input,
                        mayax_response
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        now,
                        str(user_input),
                        str(bot_response)
                    )
                )

                conn.commit()

        except Exception as e:

            log_msg(
                f"Memory Save Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )


# ============================================================
# MAYAX BRAIN
# ============================================================

class MayaxBrain:

    def __init__(
        self,
        api_key=None
    ):

        self.memory = MayaxMemory()

        self.api_key = (
            api_key or ""
        ).strip()

        self.client = None


        if not self.api_key:

            log_msg(
                "Gemini API Key Missing!"
            )

            return


        if self.api_key.startswith(
            "YOUR_"
        ):

            log_msg(
                "Gemini API Key is still a placeholder."
            )

            return


        try:

            self.client = genai.Client(
                api_key=self.api_key
            )

            log_msg(
                "Gemini Client Initialized Successfully for MAYAX."
            )

        except Exception as e:

            log_msg(
                f"Gemini Init Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )


    def process(
        self,
        command
    ):

        if not command:

            return (
                "मला तुमचा आवाज स्पष्ट ऐकू आला नाही."
            )


        command = str(command).strip()


        if not command:

            return (
                "मला तुमचा आवाज स्पष्ट ऐकू आला नाही."
            )


        if not self.client:

            return (
                "Gemini API key सेट केलेली नाही."
            )


        try:

            log_msg(
                f"MAYAX Processing: {command}"
            )


            response = (
                self.client.models.generate_content(

                    model="gemini-2.5-flash",

                    contents=command,

                    config=types.GenerateContentConfig(

                        system_instruction=(
                            "You are MAYAX, an advanced "
                            "smart AI voice assistant. "
                            "Reply naturally in the same "
                            "language as the user. "
                            "Supported languages are "
                            "Marathi, Hindi and English. "
                            "Keep normal voice responses "
                            "short and conversational."
                        )
                    )
                )
            )


            if response is None:

                log_msg(
                    "Gemini returned None."
                )

                return (
                    "मला Gemini कडून response मिळाला नाही."
                )


            reply = getattr(
                response,
                "text",
                None
            )


            if not reply:

                log_msg(
                    f"Empty Gemini response: {repr(response)}"
                )

                return (
                    "मला योग्य response मिळाला नाही."
                )


            reply = str(
                reply
            ).strip()


            self.memory.save_turn(
                command,
                reply
            )


            log_msg(
                f"MAYAX Response: {reply}"
            )


            return reply


        except Exception as e:

            log_msg(
                f"MAYAX Brain Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )

            return (
                "माझ्या AI मध्ये तात्पुरती अडचण आली आहे."
            )


# ============================================================
# VOICE CONTROLLER
# ============================================================

class MayaxVoiceController:

    def __init__(self):

        self.sample_rate = 16000

        self.command_seconds = 5

        self.is_running = True

        self.recognizer = sr.Recognizer()


        # ----------------------------------------------------
        # TTS
        # ----------------------------------------------------

        try:

            self.tts = pyttsx3.init()

            self.tts.setProperty(
                "rate",
                165
            )

            self.tts.setProperty(
                "volume",
                1.0
            )

            log_msg(
                "MAYAX Voice Engine Started."
            )

        except Exception as e:

            log_msg(
                f"TTS Setup Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )

            self.tts = None


    # ========================================================
    # SPEAK
    # ========================================================

    def speak(
        self,
        text
    ):

        if not text:

            return


        text = str(
            text
        ).strip()


        log_msg(
            f"MAYAX Speaks: {text}"
        )


        if not self.tts:

            log_msg(
                "TTS Engine unavailable."
            )

            return


        try:

            self.tts.say(
                text
            )

            self.tts.runAndWait()


        except Exception as e:

            log_msg(
                f"TTS Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )


    # ========================================================
    # LISTEN
    # ========================================================

    def listen_speech(self):

        try:

            log_msg(
                "MAYAX Listening..."
            )


            audio_data = sd.rec(

                int(
                    self.sample_rate *
                    self.command_seconds
                ),

                samplerate=self.sample_rate,

                channels=1,

                dtype="int16"
            )


            sd.wait()


            # ------------------------------------------------
            # WAV conversion
            # ------------------------------------------------

            wav_io = io.BytesIO()


            with wave.open(
                wav_io,
                "wb"
            ) as wf:

                wf.setnchannels(
                    1
                )

                wf.setsampwidth(
                    2
                )

                wf.setframerate(
                    self.sample_rate
                )

                wf.writeframes(
                    audio_data.tobytes()
                )


            wav_io.seek(0)


            # ------------------------------------------------
            # Speech Recognition
            # ------------------------------------------------

            with sr.AudioFile(
                wav_io
            ) as source:

                audio = self.recognizer.record(
                    source
                )


            languages = [
                "mr-IN",
                "hi-IN",
                "en-IN"
            ]


            for lang_code in languages:

                try:

                    text = self.recognizer.recognize_google(
                        audio,
                        language=lang_code
                    )


                    if text:

                        text = str(
                            text
                        ).strip()


                        log_msg(
                            f"Speech Detected "
                            f"({lang_code}): {text}"
                        )


                        return text


                except sr.UnknownValueError:

                    continue


                except sr.RequestError as e:

                    log_msg(
                        f"Speech API Error "
                        f"({lang_code}): {repr(e)}"
                    )

                    continue


                except Exception as e:

                    log_msg(
                        f"Speech Recognition Error "
                        f"({lang_code}): {repr(e)}"
                    )

                    continue


        except Exception as e:

            log_msg(
                f"STT Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )


        return ""


    # ========================================================
    # MAIN VOICE LOOP
    # ========================================================

    def start_listening(
        self,
        brain
    ):

        log_msg(
            "MAYAX Voice Engine Started."
        )


        self.speak(
            "MAYAX AI ready आहे."
        )


        while self.is_running:

            try:

                user_text = (
                    self.listen_speech()
                )


                if user_text:

                    response_text = (
                        brain.process(
                            user_text
                        )
                    )


                    if response_text:

                        self.speak(
                            response_text
                        )


                time.sleep(
                    0.5
                )


            except KeyboardInterrupt:

                self.is_running = False

                log_msg(
                    "MAYAX stopped by user."
                )

                break


            except Exception as e:

                log_msg(
                    f"Voice Loop Error: {repr(e)}"
                )

                log_msg(
                    traceback.format_exc()
                )

                time.sleep(
                    1
                )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    log_msg(
        "========================================"
    )

    log_msg(
        "Starting MAYAX AI..."
    )

    log_msg(
        "========================================"
    )


    # --------------------------------------------------------
    # API KEY FROM .ENV
    # --------------------------------------------------------

    api_key = os.getenv(
        "GEMINI_API_KEY",
        ""
    ).strip()


    if api_key:

        log_msg(
            "Gemini API key loaded successfully."
        )

    else:

        log_msg(
            "WARNING: GEMINI_API_KEY not found."
        )


    # --------------------------------------------------------
    # BRAIN
    # --------------------------------------------------------

    brain = MayaxBrain(
        api_key=api_key
    )


    # --------------------------------------------------------
    # VOICE
    # --------------------------------------------------------

    controller = MayaxVoiceController()


    # --------------------------------------------------------
    # VOICE THREAD
    # --------------------------------------------------------

    voice_thread = threading.Thread(

        target=controller.start_listening,

        args=(brain,),

        daemon=True
    )


    voice_thread.start()


    # --------------------------------------------------------
    # GUI
    # --------------------------------------------------------

    if MainWindow:

        try:

            app = MainWindow()

            # GUI ला Brain उपलब्ध करून देणे
            app.brain = brain


            if hasattr(
                app,
                "run"
            ):

                app.run()


            elif hasattr(
                app,
                "mainloop"
            ):

                app.mainloop()


        except Exception as e:

            log_msg(
                f"GUI Execution Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )


    else:

        log_msg(
            "GUI module not found."
        )

        try:

            voice_thread.join()

        except KeyboardInterrupt:

            controller.is_running = False

            log_msg(
                "MAYAX stopped by user."
            )
# ============================================================
# MAYAX BRAIN
# ============================================================

class MayaxBrain:

    def __init__(
        self,
        api_key=None
    ):

        self.memory = MayaxMemory()

        self.api_key = (
            api_key or ""
        ).strip()

        self.client = None


        if not self.api_key:

            log_msg(
                "Gemini API Key Missing!"
            )

            return


        if self.api_key.startswith(
            "YOUR_"
        ):

            log_msg(
                "Gemini API Key is still a placeholder."
            )

            return


        try:

            self.client = genai.Client(
                api_key=self.api_key
            )

            log_msg(
                "Gemini Client Initialized Successfully for MAYAX."
            )

        except Exception as e:

            log_msg(
                f"Gemini Init Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )


    def process(
        self,
        command
    ):

        if not command:

            return (
                "मला तुमचा आवाज स्पष्ट ऐकू आला नाही."
            )


        command = str(command).strip()


        if not command:

            return (
                "मला तुमचा आवाज स्पष्ट ऐकू आला नाही."
            )


        if not self.client:

            return (
                "Gemini API key सेट केलेली नाही."
            )


        try:

            log_msg(
                f"MAYAX Processing: {command}"
            )


            response = (
                self.client.models.generate_content(

                    model="gemini-1.5-flash",

                    contents=command,

                    config=types.GenerateContentConfig(

                        system_instruction=(
                            "You are MAYAX, an advanced "
                            "smart AI voice assistant. "
                            "Reply naturally in the same "
                            "language as the user. "
                            "Supported languages are "
                            "Marathi, Hindi and English. "
                            "Keep normal voice responses "
                            "short and conversational."
                        )
                    )
                )
            )


            if response is None:

                log_msg(
                    "Gemini returned None."
                )

                return (
                    "मला Gemini कडून response मिळाला नाही."
                )


            reply = getattr(
                response,
                "text",
                None
            )


            if not reply:

                log_msg(
                    f"Empty Gemini response: {repr(response)}"
                )

                return (
                    "मला योग्य response मिळाला नाही."
                )


            reply = str(
                reply
            ).strip()


            self.memory.save_turn(
                command,
                reply
            )


            log_msg(
                f"MAYAX Response: {reply}"
            )


            return reply


        except Exception as e:

            log_msg(
                f"MAYAX Brain Error: {repr(e)}"
            )

            log_msg(
                traceback.format_exc()
            )

            return (
                "माझ्या AI मध्ये तात्पुरती अडचण आली आहे."
            )
from src.gui.login_system import MyXAuthApp

def launch_myx_dashboard():
    """यह फ़ंक्शन लॉगिन सफल होने पर आपकी 'MyX' की मुख्य विंडो को लॉन्च करेगा।"""
    print("----------------------------------------")
    print("   Welcome to MyX AI Assistant!         ")
    print("----------------------------------------")
    
    # यहाँ आपका मुख्य UI (जैसे MainWindow, ChatPanel आदि) लोड होगा
    # उदाहरण:
    # app = MainAppWindow()
    # app.mainloop()

if __name__ == "__main__":
    # 1. पहले ऑथेंटिकेशन विंडो खुलेगी
    auth_app = MyXAuthApp(on_login_success=launch_myx_dashboard)
    
    # 2. Tkinter इवेंट लूप स्टार्ट
    auth_app.mainloop()
from src.gui.login_system import MyXAuthApp
# Agar aapka main GUI class 'mainwindow.py' ya kisi dusri file me hai toh use yahan import karein
# Example: from src.gui.mainwindow import MainWindow

def start_main_dashboard():
    """Lauches the main MyX AI Assistant dashboard after successful login."""
    print("\n==========================================")
    print("      MyX AI Assistant Dashboard Loaded   ")
    print("==========================================\n")
    
    # Yahan aapka main app UI launch hoga:
    # main_ui = MainWindow()
    # main_ui.mainloop()

if __name__ == "__main__":
    # Step 1: Launch Authentication Gatekeeper
    auth_app = MyXAuthApp(on_login_success=start_main_dashboard)
    
    # Step 2: Start GUI Loop
    auth_app.mainloop()
import getpass
from src.core.auth import AuthSystem
from src.core.brain import Brain

def start_app():
    auth = AuthSystem()
    print("=== CHITT AI Login System ===")

    attempts = 3
    while attempts > 0:
        username = input("Enter Username: ")
        password = getpass.getpass("Enter Password: ")

        if auth.login(username, password):
            print("\n[+] Login Successful! Loading CHITT Brain...\n")
            # लॉगिन यशस्वी झाल्यावर Brain मॉड्युल रन होईल
            brain = Brain()
            # येथे तुमच्या प्रोजेक्टची मुख्य रन लूप कॉल करा
            break
        else:
            attempts -= 1
            print(f"[-] Invalid Credentials. Attempts left: {attempts}\n")

    if attempts == 0:
        print("[!] System Locked. Too many failed attempts.")

if __name__ == "__main__":
    start_app()
import getpass
from src.core.auth import AuthSystem

def check_login():
    auth = AuthSystem()
    print("========================================")
    print("       CHITT / MAYAX AI Security       ")
    print("========================================")
    
    attempts = 3
    while attempts > 0:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        
        if auth.login(username, password):
            print("\n[+] Authentication Successful!\n")
            return True
        else:
            attempts -= 1
            print(f"[-] Invalid credentials. Left: {attempts}\n")
            
    print("[!] Security Lockout: Exiting application.")
    return False

if __name__ == "__main__":
    if check_login():
        # तुमचा सद्याचा main_app.py मधील AI स्टार्ट होण्याचा कोड इथे खाली सुरु होईल
        pass                                