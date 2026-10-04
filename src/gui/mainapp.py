# src/gui/mainapp.py

import os
import sys
import threading
import traceback

import customtkinter as ctk


# ============================================================
# PATH SETUP
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORTS
# ============================================================

from src.core.brain import MayaxBrain
from src.core.voice_engine import MayaxVoiceController
from src.core.vision_engine import MayaxVisionEngine
from src.gui.mainwindow import MainWindow


# ============================================================
# CONFIG
# ============================================================

ASSISTANT_NAME = "MAYAX"


# ============================================================
# CRASH LOGGER
# ============================================================

def log_crash():
    try:
        crash_file = os.path.join(PROJECT_ROOT, "crash_log.txt")

        with open(
            crash_file,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(traceback.format_exc())

        print(f"[ERROR] Crash log saved: {crash_file}")

    except Exception as e:
        print(f"[ERROR] Could not write crash log: {e}")


# ============================================================
# GEMINI KEY
# ============================================================

def get_gemini_key():

    key = os.getenv("GEMINI_API_KEY", "").strip()

    if key:
        print("[AI] Gemini API key detected.")
    else:
        print("[AI] Gemini API key not configured.")
        print("[AI] Local MAYAX system will continue.")

    return key


# ============================================================
# START VOICE ENGINE
# ============================================================

def start_voice_engine(voice_controller, brain):

    try:

        print("[VOICE] Voice engine starting...")

        voice_controller.start_listening_loop(brain)

    except Exception:

        print("[VOICE] Voice engine stopped because of an error.")
        traceback.print_exc()


# ============================================================
# MAIN SYSTEM
# ============================================================

def main():

    print()
    print("=" * 60)
    print("              MAYAX AI SYSTEM")
    print("=" * 60)
    print()

    try:

        # ----------------------------------------------------
        # 1. API KEY
        # ----------------------------------------------------

        gemini_api_key = get_gemini_key()


        # ----------------------------------------------------
        # 2. BRAIN
        # ----------------------------------------------------

        print("[SYSTEM] Initializing MAYAX Brain...")

        brain = MayaxBrain(
            api_key=gemini_api_key
        )

        print("[SYSTEM] Brain initialized.")


        # ----------------------------------------------------
        # 3. VOICE
        # ----------------------------------------------------

        print("[SYSTEM] Initializing Voice Engine...")

        voice_controller = MayaxVoiceController()

        print("[SYSTEM] Voice Engine initialized.")


        # ----------------------------------------------------
        # 4. VISION
        # ----------------------------------------------------

        print("[SYSTEM] Initializing Vision Engine...")

        vision_engine = MayaxVisionEngine()

        print("[SYSTEM] Vision Engine initialized.")


        # ----------------------------------------------------
        # 5. VOICE THREAD
        # ----------------------------------------------------

        voice_thread = threading.Thread(
            target=start_voice_engine,
            args=(
                voice_controller,
                brain
            ),
            daemon=True
        )

        voice_thread.start()

        print("[SYSTEM] Voice thread started.")


        # ----------------------------------------------------
        # 6. MAIN GUI
        # ----------------------------------------------------

        print("[SYSTEM] Starting MAYAX Control Center...")

        app = MainWindow(
            brain=brain
        )

        app.vision_engine = vision_engine


        # ----------------------------------------------------
        # 7. SYSTEM READY
        # ----------------------------------------------------

        print()
        print("=" * 60)
        print("          MAYAX AI SYSTEM READY")
        print("=" * 60)
        print()

        app.run()


    except Exception:

        print()
        print("=" * 60)
        print("              MAYAX SYSTEM ERROR")
        print("=" * 60)

        traceback.print_exc()

        log_crash()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
