# run_mayax.py
import os
import threading
from core.brain import MayaxBrain
from core.voice_engine import MayaxVoiceController
from core.vision_engine import MayaxVisionEngine
from src.gui.mainwindow import MainWindow

if __name__ == "__main__":
    print("==========================================")
    print("       MAYAX AI SYSTEM STARTING...        ")
    print("==========================================")

    # तुमची खरी API Key टाका
    API_KEY = "तुमची_खरी_GEMINI_API_KEY"

    brain = MayaxBrain(api_key=API_KEY)
    voice = MayaxVoiceController()
    vision = MayaxVisionEngine()

    threading.Thread(target=voice.start_listening_loop, args=(brain,), daemon=True).start()

    app = MainWindow(brain=brain)
    app.vision_engine = vision
    app.run()

    
