# core/automation.py
import os
import subprocess
import webbrowser
from datetime import datetime
import pyautogui
import psutil

class MayaxAutomation:
    def __init__(self):
        print("[Automation] MAYAX Automation Core Engine Initialized...")

    def handle_system_command(self, query):
        """लोकल सिस्टिम आणि ऑटोमेशन कमांड्स हाताळणे"""
        query = query.lower().strip()

        # १. वेळ आणि तारीख (Time & Date)
        if "वेळ" in query or "time" in query:
            now = datetime.now().strftime("%I:%M %p")
            return f"सध्या वेळ झाली आहे {now}"

        elif "तारीख" in query or "date" in query or "दिनांक" in query:
            today = datetime.now().strftime("%d %B %Y")
            return f"आजची तारीख आहे {today}"

        # २. ॲप्लिकेशन्स उघडणे (App Control)
        elif "notepad" in query or "नोटपॅड" in query:
            subprocess.Popen(["notepad.exe"])
            return "मी नोटपॅड सुरू करत आहे."

        elif "calculator" in query or "कॅल्क्युलेटर" in query:
            subprocess.Popen(["calc.exe"])
            return "मी कॅल्क्युलेटर सुरू करत आहे."

        elif "chrome" in query or "क्रोम" in query or "browser" in query or "ब्राउझर" in query:
            webbrowser.open("https://www.google.com")
            return "मी ब्राऊझर उघडत आहे."

        # ३. बॅटरी आणि सिस्टिम स्टेटस (Hardware Status)
        elif "battery" in query or "बॅटरी" in query:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                return f"लॅपटॉपची बॅटरी सध्या {percent} टक्के आहे."
            return "बॅटरीची माहिती मिळवता आली नाही."

        # ४. ओळख (Identity)
        elif "कोण आहेस" in query or "who are you" in query or "तुझे नाव" in query:
            return "मी MAYAX आहे, तुमचा स्मार्ट AI व्हॉईस आणि व्हिजन असिस्टंट."

        # जर लोकल कमांड नसेल तर None रिटर्न करेल
        return None
    
