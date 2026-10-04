# -*- coding: utf-8 -*-

import os
import sys
import traceback


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# UTF-8 CONSOLE
# ============================================================

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# ============================================================
# MYX CORE
# ============================================================

from src.core.brain import Brain


# ============================================================
# GUI
# ============================================================

from src.gui.mainwindow import MainWindow
from src.gui.login_system import MyXAuthApp


# ============================================================
# DASHBOARD
# ============================================================

def launch_myx_dashboard(username):
    """
    Called after successful MyX login.

    Flow:

        Login
          ↓
        Username
          ↓
        Brain(user_id=username)
          ↓
        Persistent Database
          ↓
        MyX Dashboard
    """

    print("\n==========================================")
    print(f"LOGIN SUCCESSFUL: {username}")
    print("Starting MyX Dashboard...")
    print("==========================================")

    brain = None
    app = None

    try:

        # ----------------------------------------------------
        # 1. INITIALIZE MYX BRAIN
        # ----------------------------------------------------

        print("[1/3] Initializing MyX Core...")

        # IMPORTANT:
        # The authenticated username becomes the active
        # MyX user identity for Brain + Database persistence.
        brain = Brain(
            user_id=username
        )

        print("[MyX] Brain initialized successfully.")

        # ----------------------------------------------------
        # 2. OPEN DASHBOARD
        # ----------------------------------------------------

        print("[2/3] Opening MyX Control Center...")

        app = MainWindow(
            brain=brain
        )

        print("[3/3] MyX Dashboard Ready!")

        print("------------------------------------------")
        print(f"ACTIVE USER : {username}")
        print("MYX CORE    : CONNECTED")
        print("DATABASE    : CONNECTED")
        print("PERSISTENCE : READY")
        print("DASHBOARD   : ONLINE")
        print("------------------------------------------")

        # ----------------------------------------------------
        # 3. START GUI LOOP
        # ----------------------------------------------------

        app.mainloop()

    except Exception:

        print("\n========== MYX DASHBOARD ERROR ==========")
        traceback.print_exc()
        print("=========================================\n")

    finally:

        # ----------------------------------------------------
        # 4. SAFE DATABASE CLEANUP
        # ----------------------------------------------------

        if brain is not None:

            try:
                brain.close()
                print("[MyX] Brain resources closed safely.")

            except Exception:
                print("[MyX] Warning: Brain cleanup failed.")


# ============================================================
# APPLICATION START
# ============================================================

def main():

    print("==========================================")
    print("          MyX AI SYSTEM STARTING")
    print("==========================================")

    try:

        # ----------------------------------------------------
        # LOGIN SYSTEM
        # ----------------------------------------------------

        auth_app = MyXAuthApp(
            on_login_success=launch_myx_dashboard
        )

        print("[System] Login Screen Ready")

        # ----------------------------------------------------
        # LOGIN EVENT LOOP
        # ----------------------------------------------------

        auth_app.mainloop()

    except Exception:

        print("\n========== MYX STARTUP ERROR ==========")
        traceback.print_exc()
        print("=======================================\n")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
    