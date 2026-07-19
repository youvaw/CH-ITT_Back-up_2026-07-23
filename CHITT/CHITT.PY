from datetime import datetime
import importlib
import platform
import webbrowser
from typing import Any

sr: Any = None
recognizer: Any = None
try:
    import speech_recognition as sr
    _speech_available = True
    recognizer = sr.Recognizer()
except Exception:
    _speech_available = False
    recognizer = None

try:
    _tts_mod = importlib.import_module("tts")
    _tts_speak = getattr(_tts_mod, "speak")
except Exception:
    _tts_speak = None



def speak(text, lang=None):
    if _tts_speak is None:
        if lang:
            print(f"CHITT [{lang}]: {text}")
        else:
            print(f"CHITT: {text}")
        return

    try:
        if lang is None:
            _tts_speak(text)
        else:
            try:
                _tts_speak(text, lang=lang)
            except TypeError:
                try:
                    _tts_speak(text, lang)
                except TypeError:
                    _tts_speak(text)
    except Exception:
        print(f"CHITT: {text}")


def take_command():
    if not _speech_available or recognizer is None or sr is None:
        try:
            return input("You: ")
        except EOFError:
            return ""

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except Exception as e:
            print("Listening error:", e)
            return ""

    for language in ("en-IN", "hi-IN", "mr-IN"):
        try:
            text = recognizer.recognize_google(audio, language=language)
            if text:
                return text
        except Exception:
            pass

    return ""


def get_system_info():
    info = {
        "Computer": platform.node(),
        "OS": f"{platform.system()} {platform.release()}",
        "Processor": platform.processor(),
    }

    try:
        psutil = importlib.import_module("psutil")
    except Exception:
        psutil = None

    try:
        GPUtil = importlib.import_module("GPUtil")
    except Exception:
        GPUtil = None

    if psutil:
        try:
            ram = psutil.virtual_memory()
            info["RAM"] = f"{round(ram.total / (1024**3), 2)} GB"
        except Exception:
            info["RAM"] = "Not Available"

        try:
            disk = psutil.disk_usage("/")
            info["Storage"] = f"{round(disk.total / (1024**3), 2)} GB"
        except Exception:
            info["Storage"] = "Not Available"

        try:
            battery = psutil.sensors_battery()
            info["Battery"] = f"{battery.percent}%" if battery else "Not Available"
        except Exception:
            info["Battery"] = "Not Available"
    else:
        info["RAM"] = "Not Available"
        info["Storage"] = "Not Available"
        info["Battery"] = "Not Available"

    if GPUtil:
        try:
            gpus = GPUtil.getGPUs()
            info["GPU"] = gpus[0].name if gpus else "No GPU Found"
        except Exception:
            info["GPU"] = "Unknown"
    else:
        info["GPU"] = "Not Available"

    return info


def open_google():
    webbrowser.open("https://www.google.com")


def open_youtube():
    webbrowser.open("https://www.youtube.com")


def open_gmail():
    webbrowser.open("https://mail.google.com")


def open_github():
    webbrowser.open("https://github.com")


def open_chatgpt():
    webbrowser.open("https://chat.openai.com")


def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")


def search_youtube(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")


def search_wikipedia(query):
    webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")


def greet_user():
    hour = datetime.now().hour

    if hour < 12:
        speak("Good Morning")
    elif hour < 17:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("Hello, I am CHITT AI. How can I help you?")


def shutdown():
    import os
    os.system("shutdown /s /t 5")


def restart():
    import os
    os.system("shutdown /r /t 5")


def logout():
    import os
    os.system("shutdown /l")


def lock_pc():
    import ctypes
    ctypes.windll.user32.LockWorkStation()


def sleep_pc():
    import subprocess
    subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def open_cmd():
    import os
    os.system("start cmd")


def open_notepad():
    import os
    os.system("notepad")


def open_calculator():
    import os
    os.system("calc")


def open_paint():
    import os
    os.system("mspaint")


def open_explorer():
    import os
    os.system("explorer")


def open_task_manager():
    import os
    os.system("taskmgr")


def open_control_panel():
    import os
    os.system("control")


def open_settings():
    import os
    os.system("start ms-settings:")


def open_device_manager():
    import os
    os.system("devmgmt.msc")


def main():
    greet_user()

    while True:
        command = take_command()

        if not command:
            continue

        print("You:", command)
        lower = command.lower()

        if "exit" in lower or "quit" in lower:
            speak("Goodbye")
            break

        elif "hello" in lower:
            speak("Hello! How can I help you?", "en")

        elif "नमस्ते" in command or "हिंदी" in command:
            speak("नमस्ते, मैं आपकी कैसे सहायता कर सकता हूँ?", "hi")

        elif "नमस्कार" in command or "मराठी" in command:
            speak("नमस्कार, मी तुमची कशी मदत करू शकतो?", "mr")

        elif "time" in lower:
            current = datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current}")

        elif "date" in lower:
            today = datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {today}")

        elif "system" in lower or "laptop" in lower:
            info = get_system_info()
            for key, value in info.items():
                print(f"{key}: {value}")
                speak(f"{key} {value}")

        elif "open google" in lower:
            speak("Opening Google")
            open_google()

        elif "open youtube" in lower:
            speak("Opening YouTube")
            open_youtube()

        elif "open gmail" in lower:
            speak("Opening Gmail")
            open_gmail()

        elif "open github" in lower:
            speak("Opening GitHub")
            open_github()

        elif "open chatgpt" in lower:
            speak("Opening ChatGPT")
            open_chatgpt()

        elif "search google" in lower:
            query = lower.replace("search google", "").strip()
            speak("Searching Google")
            search_google(query)

        elif "search youtube" in lower:
            query = lower.replace("search youtube", "").strip()
            speak("Searching YouTube")
            search_youtube(query)

        elif "search wikipedia" in lower:
            query = lower.replace("search wikipedia", "").strip()
            speak("Searching Wikipedia")
            search_wikipedia(query)

        elif "shutdown" in lower:
            speak("Shutting down computer")
            shutdown()

        elif "restart" in lower:
            speak("Restarting computer")
            restart()

        elif "lock computer" in lower:
            speak("Locking computer")
            lock_pc()

        elif "sleep computer" in lower:
            speak("Putting computer to sleep")
            sleep_pc()

        elif "open command prompt" in lower:
            speak("Opening Command Prompt")
            open_cmd()

        elif "open notepad" in lower:
            speak("Opening Notepad")
            open_notepad()

        elif "open calculator" in lower:
            speak("Opening Calculator")
            open_calculator()

        elif "open paint" in lower:
            speak("Opening Paint")
            open_paint()

        elif "open file explorer" in lower:
            speak("Opening File Explorer")
            open_explorer()

        elif "open task manager" in lower:
            speak("Opening Task Manager")
            open_task_manager()

        elif "open control panel" in lower:
            speak("Opening Control Panel")
            open_control_panel()

        elif "open settings" in lower:
            speak("Opening Settings")
            open_settings()

        elif "open device manager" in lower:
            speak("Opening Device Manager")
            open_device_manager()

        elif "object detection" in lower:
            speak("Starting Object Detection")
            start_object_detection()

        elif "calculate" in lower:
            expression = lower.replace("calculate", "").strip()
            if not expression:
                speak("Please provide a calculation to perform.")
            else:
                result = calculate(expression)
                print(result)
                speak(f"The answer is {result}")

        elif "play music" in lower:
            result = play_music()
            print(result)
            speak(result)

        elif "pause music" in lower:
            result = pause_music()
            speak(result)

        elif "resume music" in lower:
            result = resume_music()
            speak(result)

        elif "stop music" in lower:
            result = stop_music()
            speak(result)

        elif "weather" in lower:
            city = lower.replace("weather", "").strip()
            if city == "":
                city = "Pune"
            result = get_weather(city)
            print(result)
            speak(result)

        else:
            speak("Sorry, I don't know the answer yet.")


def calculate(command):
    import math
    command = command.lower().strip()

    try:
        if "plus" in command or "+" in command:
            a, b = map(float, command.replace("plus", "+").split("+"))
            return a + b

        elif "minus" in command or "-" in command:
            a, b = map(float, command.replace("minus", "-").split("-"))
            return a - b

        elif "multiply" in command or "*" in command:
            a, b = map(float, command.replace("multiply", "*").split("*"))
            return a * b

        elif "divide" in command or "/" in command:
            a, b = map(float, command.replace("divide", "/").split("/"))
            return a / b

        elif "square root of" in command:
            num = float(command.replace("square root of", ""))
            return math.sqrt(num)

        elif "square of" in command:
            num = float(command.replace("square of", ""))
            return num ** 2

        elif "cube of" in command:
            num = float(command.replace("cube of", ""))
            return num ** 3

        elif "power" in command:
            text = command.replace("power", "").split()
            if len(text) >= 2:
                return float(text[0]) ** float(text[1])
            return "Invalid calculation."

        else:
            return "Calculation not supported."

    except Exception:
        return "Invalid calculation."


# music.py

import os
import random
import pygame

pygame.mixer.init()

MUSIC_FOLDER = "Music"   # यहाँ अपना Music Folder दें


def play_music():
    try:
        songs = []

        for file in os.listdir(MUSIC_FOLDER):
            if file.endswith(".mp3"):
                songs.append(file)

        if len(songs) == 0:
            return "No music found."

        song = random.choice(songs)

        pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, song))
        pygame.mixer.music.play()

        return f"Playing {song}"

    except Exception as e:
        return str(e)


def pause_music():
    pygame.mixer.music.pause()
    return "Music Paused"


def resume_music():
    pygame.mixer.music.unpause()
    return "Music Resumed"


def stop_music():
    pygame.mixer.music.stop()
    return "Music Stopped"


# weather.py

import requests

API_KEY = "YOUR_OPENWEATHER_API_KEY"


def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        data = requests.get(url).json()

        if data["cod"] != 200:
            return "City not found."

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]

        return f"{city} temperature is {temp} degree Celsius. Humidity is {humidity} percent. Weather is {weather}."

    except Exception as e:
        return str(e)


# camera.py

try:
    import cv2  # type: ignore
    _cv2_available = True
except Exception:
    cv2 = None
    _cv2_available = False

try:
    import face_recognition  # type: ignore
    _face_recognition_available = True
except Exception:
    face_recognition = None
    _face_recognition_available = False

try:
    from ultralytics import YOLO  # type: ignore
    _yolo_available = True
    model = YOLO("yolov8n.pt")
except Exception:
    YOLO = None
    model = None
    _yolo_available = False


def open_camera():

    if not _cv2_available:
        return "OpenCV is not installed. Please install opencv-python."

    assert cv2 is not None

    cam = cv2.VideoCapture(0)

    while True:

        ret, frame = cam.read()

        if not ret:
            break

        cv2.imshow("CHITT Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


def start_face_recognition():

    if not _cv2_available or not _face_recognition_available:
        return "Face recognition is not available. Please install opencv-python and face_recognition."

    assert cv2 is not None

    video = cv2.VideoCapture(0)

    while True:

        ret, frame = video.read()

        if not ret:
            break

        rgb = frame[:, :, ::-1]

        assert face_recognition is not None
        faces = face_recognition.face_locations(rgb)

        for (top, right, bottom, left) in faces:

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Face Detected",
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.imshow("CHITT Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()


def start_object_detection():

    if not _cv2_available or not _yolo_available:
        return "Object detection is not available. Please install opencv-python and ultralytics."

    assert cv2 is not None

    cap = cv2.VideoCapture(0)

    if model is None:
        return "Object detection model is not loaded."

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)

        annotated = results[0].plot()

        cv2.imshow("CHITT Object Detection", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
# memory_engine.py

import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)


def recall(key):
    memory = load_memory()
    return memory.get(key, None)


def forget(key):
    memory = load_memory()

    if key in memory:
        del memory[key]
        save_memory(memory)
        return True


# Try to load external command dictionary; provide a reasonable default if missing
try:
    from command_dictionary import COMMANDS  # type: ignore
except Exception:
    COMMANDS = {
        "open google": "browser_google",
        "open youtube": "browser_youtube",
        "open camera": "camera_open",
        "play music": "music_play",
        "stop music": "music_stop",
        "weather": "weather",
        "battery": "battery",
        "system info": "hardware_info",
        "shutdown": "shutdown",
        "restart": "restart",
        "lock": "lock_pc",
    }


def find_command(text):
    text = text.lower()

    for command, action in COMMANDS.items():
        if command in text:
            return action

    return "ai_chat"

 # decision_engine.py

class DecisionEngine:

    def decide(self, command):

        command = command.lower()

        if "google" in command:
            return "browser_google"

        elif "youtube" in command:
            return "browser_youtube"

        elif "camera" in command:
            return "camera"

        elif "music" in command:
            return "music"

        elif "weather" in command:
            return "weather"

        elif "battery" in command:
            return "battery"

        elif "system" in command:
            return "hardware"

        elif "shutdown" in command:
            return "shutdown"

        else:
            return "gemini_ai"  
# reasoning_engine.py
# Using local DecisionEngine and MemoryEngine classes defined in this file

class ReasoningEngine:

    def __init__(self):
        self.memory = MemoryEngine()
        self.decision = DecisionEngine()

    def think(self, command):

        action = self.decision.decide(command)

        # use module-level remember() to persist last command to avoid
        # potential method resolution conflicts with other save definitions
        try:
            # Prefer module-level remember function to persist last command
            remember("last_command",command)
        except Exception:
            # If module-level remember fails, attempt to use MemoryEngine or
            # fall back to module-level save_memory/load_memory helpers.
            try:
                save_fn = getattr(self.memory, "save", None)
                if callable(save_fn):
                    save_fn("last_command", command)
                else:
                    # fall back to module-level memory functions
                    try:
                        mem = load_memory()
                    except Exception:
                        mem = {}
                    mem["last_command"] = command
                    try:
                        save_memory(mem)
                    except Exception:
                        # last resort: write file directly
                        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                            json.dump(mem, f, indent=4)
            except Exception as e:
                print(f"Error occurred while saving to memory: {e}")

        response = {
            "command": command,
            "action": action,
            "status": "ready"
        }

        return response
 # planning_engine.py

class PlanningEngine:

    def create_plan(self, command):

        plan = []

        command = command.lower()

        if "google" in command:
            plan.append("open_browser")
            plan.append("open_google")

        if "youtube" in command:
            plan.append("open_browser")
            plan.append("open_youtube")

        if "music" in command:
            plan.append("open_music")

        if "camera" in command:
            plan.append("open_camera")

        return plan 
    # conversation_engine.py

class ConversationEngine:

    def __init__(self):
        self.history = []

    def add(self, speaker, message):
        self.history.append({
            "speaker": speaker,
            "message": message
        })

    def last(self):
        if len(self.history) == 0:
            return None

        return self.history[-1]

    def all(self):
        return self.history

    def clear(self):
        self.history.clear()

    def build_prompt(self, latest_message=None):
        prompt = ""

        for item in self.history:
            speaker = item.get("speaker", item.get("user", "user"))
            message = item.get("message", item.get("ai", ""))

            if speaker.lower() == "assistant":
                prompt += f"Assistant: {message}\n"
            else:
                prompt += f"User: {message}\n"

        if latest_message is not None:
            last_message = ""
            if self.history:
                last_message = self.history[-1].get(
                    "message",
                    self.history[-1].get("ai", "")
                )
            if latest_message != last_message:
                prompt += f"User: {latest_message}\n"

        prompt += "Assistant:"

        return prompt
 # ai_core.py

# task_manager.py

from queue import Queue
import threading

class TaskManager:

    def __init__(self):
        self.tasks = Queue()

    def add_task(self, task_name, function, *args):
        self.tasks.put((task_name, function, args))

    def run(self):
        while not self.tasks.empty():

            task_name, function, args = self.tasks.get()

            print(f"[TASK] {task_name}")

            try:
                function(*args)
                print(f"[DONE] {task_name}")

            except Exception as e:
                print(f"[ERROR] {task_name}: {e}")

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
  # plugin_engine.py

import os
import importlib

class PluginEngine:

    def __init__(self):
        self.plugins = {}

    def load_plugins(self):

        folder = "plugins"

        if not os.path.exists(folder):
            os.mkdir(folder)

        for file in os.listdir(folder):

            if file.endswith(".py"):

                name = file[:-3]

                module = importlib.import_module(f"plugins.{name}")

                self.plugins[name] = module

    def execute(self, name):

        if name in self.plugins:
            self.plugins[name].run()  
        else:
            speak("Sorry, I don't know the answer yet.")


# Removed duplicate speak function - using original speak function defined at line 24


try:
    import importlib
    module = importlib.import_module("gemini_ai")
    ask_gemini = getattr(module, "ask_gemini", lambda prompt: "Gemini AI function not found.")
except (ImportError, ModuleNotFoundError):
    ask_gemini = lambda prompt: "Gemini AI module not found."


class CHITTCore:

    def __init__(self):
        self.decision = DecisionEngine()
        self.memory = MemoryEngine()
        self.planner = PlanningEngine()
        self.reasoning = ReasoningEngine()

    def _persist_last_command(self, command):
        try:
            remember("last_command", command)
        except Exception:
            try:
                save_fn = getattr(self.memory, "save", None)
                if callable(save_fn):
                    save_fn("last_command", command)
                else:
                    raise AttributeError("MemoryEngine.save is unavailable")
            except Exception:
                try:
                    mem = load_memory()
                    mem["last_command"] = command
                    save_memory(mem)
                except Exception:
                    pass

    def process(self, command):
        self._persist_last_command(command)
        action = self.decision.decide(command)
        plan = self.planner.create_plan(command)
        result = self.reasoning.think(command)

        return {
            "command": command,
            "action": action,
            "plan": plan,
            "reason": result
        }

_brain = None

def get_brain():
    global _brain
    if _brain is None:
        _brain = CHITTCore()
    return _brain

def process_command(command, speak):

    result = get_brain().process(command)

    action = result["action"]

    if action == "browser_google":
        open_google()
        speak("Opening Google")

    elif action == "browser_youtube":
        open_youtube()
        speak("Opening YouTube")

    elif action == "music":
        play_music()
        speak("Playing music")

    elif action == "camera":
        open_camera()
        speak("Opening camera")

    elif action == "weather":
        weather = get_weather("Pune")
        speak(weather)

    else:
        answer = ask_gemini(command)
        speak(answer)        
        # scheduler_engine.py

import time
import threading
from datetime import datetime

class SchedulerEngine:

    def __init__(self):
        self.jobs = []

    def add_job(self, job_time, callback, *args):
        self.jobs.append({
            "time": job_time,
            "callback": callback,
            "args": args,
            "done": False
        })

    def run(self):
        while True:

            now = datetime.now().strftime("%H:%M")

            for job in self.jobs:

                if job["done"]:
                    continue

                if now == job["time"]:

                    try:
                        job["callback"](*job["args"])
                        job["done"] = True

                    except Exception as e:
                        print(e)

            time.sleep(20)

    def start(self):

        thread = threading.Thread(target=self.run)

        thread.daemon = True

        thread.start()

scheduler = SchedulerEngine()

scheduler.add_job(
    "09:00",
    process_command,
    "open google",
    speak
)

scheduler.add_job(
    "21:00",
    process_command,
    "play music",
    speak
)

scheduler.start()
# notification_engine.py

try:
    # importlib used to avoid static import errors in editors when plyer
    # is not installed in the environment running static analysis.
    _plyer = importlib.import_module("plyer")
    notification = getattr(_plyer, "notification", None)
except Exception:
    notification = None

class NotificationEngine:

    def __init__(self):
        self.app_name = "CHITT AI"

    def show(self, title, message):
        if notification is None:
            print(f"{title}: {message}")
            return

        notification.notify(
            title=title,
            message=message,
            app_name=self.app_name,
            timeout=8
        )

    def info(self, message):
        self.show("Information", message)

    def warning(self, message):
        self.show("Warning", message)

    def success(self, message):
        self.show("Success", message)

    def error(self, message):
        self.show("Error", message)

notify = NotificationEngine()

notify.success("CHITT AI Started Successfully")
notify.info("Opening Google")
speak("Opening Google")
open_google()
# desktop_controller.py

import pyautogui
import subprocess
import os

class DesktopController:

    def open_app(self, path):
        try:
            subprocess.Popen(path)
            return True
        except Exception as e:
            print(e)
            return False

    def open_folder(self, path):
        try:
            os.startfile(path)
            return True
        except Exception as e:
            print(e)
            return False

    def press(self, key):
        pyautogui.press(key)

    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)

    def type_text(self, text):
        pyautogui.write(text, interval=0.03)

    def click(self, x, y):
        pyautogui.click(x, y)

    def move(self, x, y):
        pyautogui.moveTo(x, y, duration=0.2)

    def screenshot(self, file="screen.png"):
        pyautogui.screenshot(file)

desktop = DesktopController()

desktop.press("win")
desktop.type_text("notepad")
desktop.press("enter")
# system_monitor.py

import psutil

class SystemMonitor:

    def cpu(self):
        return psutil.cpu_percent(interval=1)

    def ram(self):
        return psutil.virtual_memory().percent

    def battery(self):
        battery = psutil.sensors_battery()
        if battery:
            return battery.percent
        return None

    def disk(self):
        return psutil.disk_usage("/").percent
# plugin_manager.py

import os
import importlib.util

class PluginManager:

    def __init__(self, plugin_folder="plugins"):
        self.plugin_folder = plugin_folder
        self.plugins = {}

    def load_plugins(self):

        if not os.path.exists(self.plugin_folder):
            os.makedirs(self.plugin_folder)

        for file in os.listdir(self.plugin_folder):

            if file.endswith(".py"):

                name = file[:-3]

                path = os.path.join(self.plugin_folder, file)

                spec = importlib.util.spec_from_file_location(name, path)

                if spec is None:
                    continue

                module = importlib.util.module_from_spec(spec)

                if spec.loader is not None:
                    spec.loader.exec_module(module)

                    self.plugins[name] = module

                print(f"Loaded Plugin: {name}")

    def execute(self, name, *args):

        if name in self.plugins:

            if hasattr(self.plugins[name], "run"):

                return self.plugins[name].run(*args)

        return None

plugins = PluginManager()

plugins.load_plugins()

result = plugins.execute("calculator", 10, 20)

print(result)
# security_engine.py

import hashlib

class SecurityEngine:

    def __init__(self):
        self.password_hash = None

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        if self.password_hash is None:
            return False

        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

    def authorize(self, action):

        protected = [
            "shutdown",
            "restart",
            "delete_file",
            "format_disk",
            "lock_pc"
        ]

        return action not in protected

security = SecurityEngine()

security.set_password("1234")

if security.verify_password("1234"):
    print("Access Granted")
else:
    print("Access Denied")
    # event_engine.py

from collections import defaultdict

class EventEngine:

    def __init__(self):
        self.events = defaultdict(list)

    def register(self, event_name, callback):
        self.events[event_name].append(callback)

    def trigger(self, event_name, *args, **kwargs):

        if event_name in self.events:

            for callback in self.events[event_name]:

                try:
                    callback(*args, **kwargs)

                except Exception as e:
                    print(f"[EVENT ERROR] {e}")

    def remove(self, event_name, callback):

        if callback in self.events.get(event_name, []):

            self.events[event_name].remove(callback)

            if not self.events[event_name]:
                del self.events[event_name]

events = EventEngine()

def on_start():
    print("CHITT Started")

def on_command(command):
    print("Command:", command)

events.register("startup", on_start)
events.register("command", on_command)

events.trigger("startup")
events.trigger("command", "Open Google")
# dashboard.py

import sys
try:
    from PySide6.QtWidgets import (  # type: ignore
        QApplication,
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QLabel,
        QTextEdit,
        QPushButton
    )
    from PySide6.QtCore import Qt  # type: ignore
    PYSIDE_AVAILABLE = True
except ImportError:
    PYSIDE_AVAILABLE = False
    QApplication = None
    QMainWindow = None
    QWidget = None
    QVBoxLayout = None
    QLabel = None
    QTextEdit = None
    QPushButton = None
    Qt = None

if PYSIDE_AVAILABLE and QMainWindow is not None:
    class CHITTDashboard(QMainWindow):

        def __init__(self):
            super().__init__()

            self.setWindowTitle("CHITT AI")
            self.resize(1000, 700)

            central = QWidget() if QWidget is not None else None
            # central should be a QWidget here; assert for the type checker
            assert central is not None
            self.setCentralWidget(central)

            assert QVBoxLayout is not None
            layout = QVBoxLayout()

            # QLabel may be None in type checker; assert it's available before calling
            assert QLabel is not None
            self.title = QLabel()
            # Guard Qt usage for type-checkers and optional availability
            if Qt is not None:
                # Different Qt bindings expose alignment constants differently
                align = getattr(Qt, "AlignCenter", None)
                if align is None:
                    # PyQt6/PySide6 may use AlignmentFlag.AlignCenter
                    alignment_flag = getattr(Qt, "AlignmentFlag", None)
                    align = getattr(alignment_flag, "AlignCenter", None) if alignment_flag is not None else None
                if align is not None:
                    self.title.setAlignment(align)
            self.title.setStyleSheet("font-size:28px;font-weight:bold;")

            self.chat = QTextEdit() if QTextEdit is not None else None
            if self.chat is not None:
                self.chat.setReadOnly(True)

            self.status = QLabel("Status : Ready") if QLabel is not None else None

            self.button = QPushButton("Start Listening") if QPushButton is not None else None

            assert self.title is not None
            assert self.chat is not None
            assert self.status is not None
            assert self.button is not None

            layout.addWidget(self.title)
            layout.addWidget(self.chat)
            layout.addWidget(self.status)
            layout.addWidget(self.button)

        def add_message(self, sender, message):
            if self.chat is not None:
                self.chat.append(f"<b>{sender}:</b> {message}")

        def set_status(self, text):
            if self.status is not None:
                self.status.setText(f"Status : {text}")

else:
    CHITTDashboard = None  # type: ignore


if __name__ == "__main__":
    if not PYSIDE_AVAILABLE:
        print("PySide6 is not available. Install it to run the GUI.")
        sys.exit(1)

    assert CHITTDashboard is not None

    assert QApplication is not None
    app = QApplication(sys.argv)

    window = CHITTDashboard()
    window.show()

    window.add_message("CHITT", "Hello! I am ready.")
    window.set_status("Listening")

    sys.exit(app.exec())
    # voice_engine.py

import speech_recognition as sr
import pyttsx3
import threading

class VoiceEngine:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 175)

        # getProperty may return None or a non-iterable in some environments;
        # ensure we have an iterable (empty list fallback) before converting to list
        voices_prop = self.engine.getProperty("voices")
        if voices_prop is None:
            voices = []
        else:
            try:
                voices = list()
            except TypeError:
                voices = []

        if voices:
            self.engine.setProperty("voice", voices[0].id)

    def speak(self, text):

        print("CHITT:", text)

        self.engine.say(text)

        self.engine.runAndWait()

    def listen(self):

        with sr.Microphone() as source:

            print("Listening...")

            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = self.recognizer.listen(source)

        try:

            text = self.recognizer.recognize_google(audio)

            print("You:", text)

            return text.lower()

        except Exception:

            return ""

    def speak_async(self, text):

        threading.Thread(
            target=self.speak,
            args=(text,),
            daemon=True
        ).start()

class WakeWord:

    def __init__(self):

        self.words = [
            "hey chitt",
            "hello chitt",
            "ok chitt",
            "chitt"
        ]

    def detected(self, text):

        text = text.lower()

        for word in self.words:

            if word in text:
                return True

        return False

# config.py

from dataclasses import dataclass

@dataclass
class AIConfig:

    APP_NAME = "CHITT AI"

    VERSION = "1.0"

    AUTHOR = "Manoj Sharma"

    LANGUAGE = "en"

    OFFLINE_MODE = False

    WAKE_WORD = "hey chitt"

    GEMINI_MODEL = "gemini-2.5-flash"

    VOICE_RATE = 175

    MEMORY_FILE = "memory.json"

    LEARNING_FILE = "learning.json"

    LOG_FILE = "logs/chitt.log"

    PLUGIN_FOLDER = "plugins"

    DATA_FOLDER = "data"

    CAMERA_INDEX = 0

    WEATHER_CITY = "Pune"

    MAX_HISTORY = 100

    DEBUG = True

config = AIConfig()
   # logger.py

import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/chitt.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

class Logger:

    @staticmethod
    def info(message):
        logging.info(message)
        print(message)

    @staticmethod
    def error(message):
        logging.error(message)
        print(message)

    @staticmethod
    def warning(message):
        logging.warning(message)
        print(message)    
        # startup.py

# Logger is defined above in this file; no external import needed

class Startup:

    def boot(self):

        Logger.info("Loading AI Core...")

        Logger.info("Loading Memory...")

        Logger.info("Loading Voice Engine...")

        Logger.info("Loading Dashboard...")

        Logger.info("Loading Plugins...")

        Logger.info("CHITT AI Ready")
         # ===========================
# CHITT AI Professional v1.0
# main.py (Part 1)
# ===========================

# Startup, config, and Logger are defined earlier in this file.

# from voice_engine import VoiceEngine
# from wake_word import WakeWord

# from ai_core import CHITTCore

# from dashboard import CHITTDashboard

# from notification_engine import NotificationEngine

# from plugin_manager import PluginManager

# from scheduler_engine import SchedulerEngine

# from task_manager import TaskManager

# from automation_engine import AutomationEngine

# from system_monitor import SystemMonitor

# SecurityEngine is defined later in this file, no external import is needed
# from security_engine import SecurityEngine

import threading
import sys

from PySide6.QtWidgets import QApplication


class AutomationEngine:
    def __init__(self):
        pass


class CHITT:

    def __init__(self):

        Logger.info("Starting CHITT AI")

        Startup().boot()

        self.voice = VoiceEngine()

        self.wake = WakeWord()

        self.ai = CHITTCore()

        self.notify = NotificationEngine()

        self.plugins = PluginManager()

        self.scheduler = SchedulerEngine()

        self.tasks = TaskManager()

        self.automation = AutomationEngine()

        self.monitor = SystemMonitor()

        self.security = SecurityEngine()

        self.plugins.load_plugins()

        self.scheduler.start()

        Logger.info("Initialization Complete")
    def voice_loop(self):

        while True:

            command = self.voice.listen()

            if not command:
                continue

            Logger.info(command)

            if self.wake.detected(command):

                self.voice.speak("Yes Sir.")

                continue

            result = self.ai.process(command)

            print(result)

    def dashboard(self):

        # Ensure Qt is available and QApplication was imported successfully
        if QApplication is None or CHITTDashboard is None:
            Logger.info("Dashboard not available: PySide6 not installed or dashboard unavailable")
            return

        try:
            app = QApplication(sys.argv)
        except Exception as e:
            Logger.error(f"Failed to create QApplication: {e}")
            return

        window = CHITTDashboard()

        window.show()

        sys.exit(app.exec())

    def run(self):

        voice = threading.Thread(target=self.voice_loop)

        voice.daemon = True

        voice.start()

        self.dashboard()


if __name__ == "__main__":

    CHITT().run()
    # ===========================
# main.py Part-2
# Command Processing
# ===========================

from command_router import process_command # pyright: ignore[reportMissingImports]
from conversation_engine import ConversationEngine # pyright: ignore[reportMissingImports]
try:
    from gemini_ai import ask_gemini # pyright: ignore[reportMissingImports]
except Exception: # pyright: ignore[reportMissingImports]
    # Fallback if gemini_ai is not available: define a simple stub
    def ask_gemini(prompt: str) -> str:
        """Fallback ask_gemini when gemini_ai import fails."""
        Logger.warning(f"gemini_ai not available, returning empty response for prompt: {prompt}")
        return ""

class CHITTConversation:

    def __init__(self):

        self.chat = ConversationEngine()

        self.voice = VoiceEngine()

        self.wake = WakeWord()

        self.running = True

        try:
            self.scheduler
        except Exception:
            try:
                self.scheduler = scheduler
            except Exception:
                self.scheduler = SchedulerEngine()

        try:
            self.monitor
        except Exception:
            self.monitor = SystemMonitor()

    def initialize(self):

        # Preserve existing components if they are already configured
        try:
            self.chat
        except Exception:
            self.chat = ConversationEngine()

        try:
            self.voice
        except Exception:
            self.voice = VoiceEngine()

        try:
            self.wake
        except Exception:
            self.wake = WakeWord()

        self.running = True

        Logger.info("Conversation Engine Loaded")
        # ensure scheduler and monitor exist for thread management
        try:
            self.scheduler  # if already set, leave as is
        except Exception:
            # use the global scheduler if available, otherwise create a new one
            try:
                self.scheduler = scheduler
            except Exception:
                self.scheduler = SchedulerEngine()

        try:
            self.monitor  # ensure monitor exists
        except Exception:
            self.monitor = SystemMonitor()

    def handle_conversation(self, command):

        # process_command expects a speak callback; provide the voice engine's speak
        response = process_command(command, self.voice.speak)

        if response is None:

            response = ask_gemini(command)

        self.chat.add(command, response)

        self.voice.speak(response)

        return response

    def ai_loop(self):

        while self.running:

            command = self.voice.listen()

            if command == "":
                continue

            if self.wake.detected(command):

                self.voice.speak("Yes, I am listening.")

                continue

            self.handle_conversation(command)

    def start_threads(self):

        threading.Thread(
            target=self.ai_loop,
            daemon=True
        ).start()

        threading.Thread(
            target=self.scheduler.run,
            daemon=True
        ).start()

        threading.Thread(
            target=self.monitor_loop,
            daemon=True
        ).start()

    def monitor_loop(self):

        while True:

            cpu = self.monitor.cpu()

            ram = self.monitor.ram()

            Logger.info(f"CPU {cpu}%")

            Logger.info(f"RAM {ram}%")

            time.sleep(5)

    def run(self):

        self.initialize()

        self.start_threads()

        # Open dashboard if available; otherwise just log status
        try:
            self.dashboard()
        except Exception:
            # provide a fallback dashboard method
            self.open_dashboard()

    def dashboard(self):

        # If CHITTDashboard is available (from dashboard.py), open it with a QApplication
        try:
            if CHITTDashboard is None:
                raise RuntimeError("Dashboard not available")

            app = None
            qapp_cls = globals().get('QApplication')
            if qapp_cls is not None and getattr(qapp_cls, 'instance', None) is not None:
                try:
                    app = qapp_cls.instance()
                except Exception:
                    app = None

            if app is None:
                if 'QApplication' in globals() and callable(QApplication):
                    app = QApplication(sys.argv)
                else:
                    from PySide6.QtWidgets import QApplication as _QApp  # type: ignore
                    app = _QApp(sys.argv)

            window = CHITTDashboard()
            window.show()
            # Run the Qt event loop; this will block until window is closed
            app.exec()

        except Exception as e:
            Logger.info(f"Dashboard not started: {e}")

    def open_dashboard(self):
        Logger.info("Dashboard not available; continuing without GUI")
        # ==========================
# AI Dispatcher
# ==========================

from concurrent.futures import ThreadPoolExecutor
# Logger is defined earlier in this file; no external import needed

class AIDispatcher:

    def __init__(self, chitt):

        self.chitt = chitt

        self.executor = ThreadPoolExecutor(max_workers=8)

    def process(self, command):

        Logger.info(f"Command : {command}")

        future = self.executor.submit(
            self.chitt.handle_conversation,
            command
        )

        return future.result()
    # ==========================
# background_services.py
# ==========================

import threading

class BackgroundServices:

    def __init__(self, chitt):

        self.chitt = chitt

    def start(self):

        threading.Thread(
            target=self.chitt.monitor_loop,
            daemon=True
        ).start()

        threading.Thread(
            target=self.chitt.scheduler.run,
            daemon=True
        ).start()

        threading.Thread(
            target=self.chitt.voice_loop,
            daemon=True
        ).start()
 # ==========================
# ai_router.py
# ==========================

class AIRouter:

    def __init__(self):

        self.modules = {}

    def register(self, name, callback):

        self.modules[name] = callback

    def execute(self, module, command):

        if module in self.modules:

            return self.modules[module](command)

        return 
  # module_manager.py

class ModuleManager:

    def __init__(self):
        self.modules = {}

    def register(self, name, module):
        self.modules[name] = module

    def get(self, name):
        return self.modules.get(name)

    def exists(self, name):
        return name in self.modules

    def start_all(self):

        for name, module in self.modules.items():

            if hasattr(module, "start"):

                try:

                    module.start()

                    print(f"[OK] {name}")

                except Exception as e:

                    print(f"[ERROR] {name} -> {e}")

    def stop_all(self):

        for name, module in self.modules.items():

            if hasattr(module, "stop"):

                try:

                    module.stop()

                except Exception:

                    pass

    def status(self):

        return list(self.modules.keys())

# resource_manager.py

import psutil

class ResourceManager:

    def cpu(self):
        return psutil.cpu_percent()

    def ram(self):
        return psutil.virtual_memory().percent

    def disk(self):
        return psutil.disk_usage("/").percent

    def battery(self):
        battery = psutil.sensors_battery()

        if battery:
            return battery.percent

        return None

    def network(self):
        return psutil.net_io_counters()  
    # ===============================
# CHITT AI Professional
# Main Integration
# ===============================

import os
import sys
import importlib

# Ensure current file directory is on sys.path for local imports
base_dir = os.path.dirname(__file__)
if base_dir and base_dir not in sys.path:
    sys.path.append(base_dir)

# Try direct import first, fall back to importlib to provide clearer error handling
import importlib

try:
    from ai_core import CHITTCore  # pyright: ignore[reportMissingImports]
except ImportError:
    CHITTCore = importlib.import_module("ai_core").CHITTCore

try:
    from voice_engine import VoiceEngine  # pyright: ignore[reportMissingImports]
except ImportError:
    VoiceEngine = importlib.import_module("voice_engine").VoiceEngine

try:
    from plugin_manager import PluginManager  # pyright: ignore[reportMissingImports]
except ImportError:
    PluginManager = importlib.import_module("plugin_manager").PluginManager

try:
    from notification_engine import NotificationEngine  # pyright: ignore[reportMissingImports]
except ImportError:
    NotificationEngine = importlib.import_module("notification_engine").NotificationEngine

try:
    from dashboard import CHITTDashboard  # pyright: ignore[reportMissingImports]
except ImportError:
    CHITTDashboard = importlib.import_module("dashboard").CHITTDashboard
except Exception:
    CHITTDashboard = importlib.import_module('dashboard').CHITTDashboard
from system_monitor import SystemMonitor # pyright: ignore[reportMissingImports]
# SecurityEngine is defined in this file; no external import required

class CHITTApplication:

    def __init__(self):

        self.modules = ModuleManager()

        self.ai = CHITTCore()

        self.voice = VoiceEngine()

        self.dashboard = CHITTDashboard()

        self.plugins = PluginManager()

        self.notification = NotificationEngine()

        self.monitor = SystemMonitor()

        self.security = SecurityEngine()

        self.register_modules()

    def register_modules(self):

        self.modules.register("AI", self.ai)
        self.modules.register("Voice", self.voice)
        self.modules.register("Dashboard", self.dashboard)
        self.modules.register("Plugins", self.plugins)
        self.modules.register("Monitor", self.monitor)
        self.modules.register("Security", self.security)

    def start(self):

        self.plugins.load_plugins()

        self.modules.start_all()

        self.notification.success("CHITT AI Started")

        self.voice.speak("CHITT AI is ready.")

        self.dashboard.show()
    def run_forever(self):

        while True:

            command = self.voice.listen()

            if not command:
                continue

            result = self.ai.process(command)

            response = result.get("response", "Done")

            self.voice.speak(response)

            self.dashboard.add_message("You", command)

            self.dashboard.add_message("CHITT", response)

# ===============================
# main.py Part-5
# Startup Manager
# ===============================

class StartupManager:

    def __init__(self, app):
        self.app = app

    def initialize(self):

        Logger.info("Loading Configuration...")
        Logger.info("Loading Memory Engine...")
        Logger.info("Loading AI Core...")
        Logger.info("Loading Voice Engine...")
        Logger.info("Loading Dashboard...")
        Logger.info("Loading Plugins...")
        Logger.info("Loading Scheduler...")
        Logger.info("Loading Automation...")
        Logger.info("Loading Notification Engine...")
        Logger.info("Loading Security Engine...")
        Logger.info("Loading Vision Engine...")

        self.app.plugins.load_plugins()

        self.app.modules.start_all()

        self.app.notification.success("CHITT AI Ready")

        self.app.voice.speak("Hello. CHITT AI is ready.")
import threading
import time

class HealthMonitor:

    def __init__(self, app):

        self.app = app

    def run(self):

        while True:

            cpu = self.app.monitor.cpu()

            ram = self.app.monitor.ram()

            Logger.info(f"CPU {cpu}%")

            Logger.info(f"RAM {ram}%")

            time.sleep(5)

    def start(self):

        threading.Thread(
            target=self.run,
            daemon=True
        ).start()


class AIServiceManager:

    def __init__(self):

        self.services = {}

    def register(self, name, service):

        self.services[name] = service

    def start(self):

        for service in self.services.values():

            if hasattr(service, "start"):

                service.start()

# intent_engine.py

class IntentEngine:

    def __init__(self):
        self.intents = {
            "open_google": [
                "open google",
                "google",
                "start google"
            ],
            "open_youtube": [
                "open youtube",
                "youtube"
            ],
            "weather": [
                "weather",
                "temperature",
                "forecast"
            ],
            "play_music": [
                "play music",
                "music",
                "song"
            ],
            "shutdown": [
                "shutdown",
                "turn off computer"
            ]
        }

    def detect(self, text):

        text = text.lower()

        for intent, keywords in self.intents.items():

            for keyword in keywords:

                if keyword in text:
                    return intent

        return "chat"

intent_engine = IntentEngine()

command = take_command()

intent = intent_engine.detect(command)

print(intent)

if intent == "open_google":
    open_google()

elif intent == "open_youtube":
    open_youtube()

elif intent == "play_music":
    play_music()

elif intent == "weather":
    speak(())

else:
    answer = ask_gemini(command)
    speak(answer)
 # language_engine.py

from langdetect import detect
from deep_translator import GoogleTranslator

class LanguageEngine:

    def __init__(self):
        self.supported = {
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi"
        }

    def detect_language(self, text):

        try:
            lang = detect(text)

            if lang in self.supported:
                return lang

            return "en"

        except Exception:
            return "en"

    def get_language_name(self, code):
        return self.supported.get(code, "English")

class TranslatorEngine:

    def translate(self, text, target="en"):

        try:
            return GoogleTranslator(
                source="auto",
                target=target
            ).translate(text)

        except Exception:
            return text

language_engine = LanguageEngine()
translator_engine = TranslatorEngine()

# task_executor.py

from queue import Queue
import threading

class TaskExecutor:

    def __init__(self):
        self.queue = Queue()
        self.running = True

        worker = threading.Thread(target=self.worker, daemon=True)
        worker.start()

    def add_task(self, func, *args, **kwargs):
        self.queue.put((func, args, kwargs))

    def worker(self):

        while self.running:

            func, args, kwargs = self.queue.get()

            try:
                func(*args, **kwargs)

            except Exception as e:
                print(f"[TASK ERROR] {e}")

            finally:
                self.queue.task_done()

    def stop(self):
        self.running = False

executor = TaskExecutor()

executor.add_task(speak, "Hello, I am CHITT AI")

executor.add_task(open_google)

executor.add_task(play_music)
executor.add_task(process_command, "open google")

executor.add_task(process_command, "open youtube")

executor.add_task(process_command, "play music")
# memory_engine.py

import json
import os

class MemoryEngine:

    def __init__(self, file_name="memory.json"):

        self.file_name = file_name

        self.memory = {}

        self.load()

    def load(self):

        if os.path.exists(self.file_name):

            try:

                with open(self.file_name, "r", encoding="utf-8") as f:

                    self.memory = json.load(f)

            except:

                self.memory = {}

    def save(self):

        with open(self.file_name, "w", encoding="utf-8") as f:

            json.dump(
                self.memory,
                f,
                indent=4,
                ensure_ascii=False
            )

    def set(self, key, value):

        self.memory[key] = value

        self.save()

    def get(self, key, default=None):

        return self.memory.get(key, default)

    def remove(self, key):

        if key in self.memory:

            del self.memory[key]

            self.save()

    def clear(self):

        self.memory.clear()

        self.save()

    def all(self):

        return self.memory


def _demo():
    memory = MemoryEngine()

    memory.set("user_name", "Manoj")
    memory.set("language", "Hindi")

    print(memory.get("user_name"))
    print(memory.all())


if __name__ == "__main__":
    _demo()
 # learning_engine.py

import json
import os

class LearningEngine:

    def __init__(self, database="learning.json"):

        self.database = database
        self.data = {}

        self.load()

    def load(self):

        if os.path.exists(self.database):

            with open(self.database, "r", encoding="utf-8") as file:

                self.data = json.load(file)

    def save(self):

        with open(self.database, "w", encoding="utf-8") as file:

            json.dump(
                self.data,
                file,
                indent=4,
                ensure_ascii=False
            )

    def learn(self, question, answer):

        self.data[question.lower()] = answer

        self.save()

    def search(self, question):

        return self.data.get(question.lower())

    def knows(self, question):

        return question.lower() in self.data

brain = LearningEngine()

brain.learn(
    "what is your name",
    "My name is CHITT AI."
)

print(brain.search("what is your name")) 
answer = brain.search(command)

if answer:

    speak(answer)

else:

    answer = ask_gemini(command)

    brain.learn(command, answer)

    speak(answer)
   # knowledge_base.py

import json
import os

class KnowledgeBase:

    def __init__(self, file="knowledge.json"):
        self.file = file
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def add(self, question, answer):
        self.data[question.lower()] = answer
        self.save()

    def find(self, question):
        return self.data.get(question.lower())

    def delete(self, question):
        if question.lower() in self.data:
            del self.data[question.lower()]
            self.save()

    def all(self):
        return self.data

kb = KnowledgeBase()

kb.add(
    "who are you",
    "I am CHITT AI."
)

print(kb.find("who are you"))
answer = kb.find(command)

if answer:
    speak(answer)

else:
    answer = ask_gemini(command)

    kb.add(command, answer)

    speak(answer)
    # context_engine.py

from collections import deque

class ContextEngine:

    def __init__(self, max_context=10):
        self.context = deque(maxlen=max_context)

    def add(self, speaker, message):
        self.context.append({
            "speaker": speaker,
            "message": message
        })

    def last(self):
        if self.context:
            return self.context[-1]
        return None

    def history(self):
        return list(self.context)

    def clear(self):
        self.context.clear()

    def prompt(self):
        text = ""
        for item in self.context:
            text += f"{item['speaker']}: {item['message']}\n"
        return text

# Initialize and use context engine
context = ContextEngine()
context.add("User", "Open Google")
context.add("CHITT", "Opening Google")
print(context.prompt())

context.add("User", command)
answer = ask_gemini(context.prompt())
context.add("CHITT", answer)
speak(answer)
# brain_manager.py

# The required engine classes are defined in this single-file bundle,
# so external imports are not needed here.
# from memory_engine import MemoryEngine
# from learning_engine import LearningEngine
# from context_engine import ContextEngine
# from decision_engine import DecisionEngine
# from planning_engine import PlanningEngine
# from intent_engine import IntentEngine
# from knowledge_base import KnowledgeBase

class BrainManager:

    def __init__(self):

        self.memory = MemoryEngine()

        self.learning = LearningEngine()

        self.context = ContextEngine()

        self.decision = DecisionEngine()

        self.planning = PlanningEngine()

        self.intent = IntentEngine()

        self.knowledge = KnowledgeBase()

    def process(self, command):

        self.context.add("User", command)

        intent = self.intent.detect(command)

        answer = self.knowledge.find(command)

        if answer:

            self.context.add("CHITT", answer)

            return {
                "intent": intent,
                "response": answer
            }

        action = self.decision.decide(command)

        plan = self.planning.create_plan(command)

        return {
            "intent": intent,
            "action": action,
            "plan": plan,
            "response": None
        }

    def learn(self, question, answer):

        self.learning.learn(question, answer)

        self.knowledge.add(question, answer)

    def remember(self, key, value):

        self.memory.set(key, value)

    def recall(self, key):

        return self.memory.get(key)

brain = BrainManager()

result = brain.process(command)

if result["response"]:

    speak(result["response"])

else:

    answer = ask_gemini(command)

    brain.learn(command, answer)

    speak(answer)
# plugin_loader.py

import os
import importlib.util

class PluginLoader:

    def __init__(self, folder="plugins"):
        self.folder = folder
        self.plugins = {}

    def load(self):

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        for file in os.listdir(self.folder):

            if not file.endswith(".py"):
                continue

            path = os.path.join(self.folder, file)

            name = file[:-3]

            spec = importlib.util.spec_from_file_location(name, path)

            if spec is None or spec.loader is None:
                print(f"[PLUGIN] Skipping {name}: failed to create spec or loader")
                continue

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            self.plugins[name] = module

            print(f"[PLUGIN] Loaded {name}")

    def execute(self, plugin_name, *args):

        plugin = self.plugins.get(plugin_name)

        if plugin and hasattr(plugin, "run"):

            return plugin.run(*args)

        return None

    def list_plugins(self):

        return list(self.plugins.keys())

def run(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Calculation Error"

loader = PluginLoader()

loader.load()

answer = loader.execute("calculator", "10+20*5")

print(answer)
         # core/event_bus.py

from collections import defaultdict
import threading

class EventBus:

    def __init__(self):
        self.listeners = defaultdict(list)
        self.lock = threading.Lock()

    def subscribe(self, event_name, callback):
        with self.lock:
            self.listeners[event_name].append(callback)

    def unsubscribe(self, event_name, callback):
        with self.lock:
            if callback in self.listeners[event_name]:
                self.listeners[event_name].remove(callback)

    def publish(self, event_name, data=None):

        callbacks = self.listeners.get(event_name, [])

        for callback in callbacks:
            try:
                callback(data)
            except Exception as e:
                print(f"[EVENT ERROR] {event_name}: {e}")

bus = EventBus()

def on_voice_command(data):
    print("Command:", data)

bus.subscribe("voice.command", on_voice_command)

bus.publish("voice.command", "Open Google")
# voice listen not available here; set command to None (or implement voice.listen elsewhere)
command = None

bus.publish("voice.command", command)
def update_chat(command):
    # Try to find a dashboard instance from globals or the service registry
    try:
        db = globals().get('dashboard')
        if db is None and 'registry' in globals():
            try:
                db = globals()['registry'].get('dashboard')
            except Exception:
                db = None
        if db:
            db.add_message("User", command)
    except Exception as e:
        print(f"[UPDATE_CHAT ERROR] {e}")

bus.subscribe("voice.command", update_chat)
def process(command):

    brain_instance = globals().get("brain")

    if brain_instance is None or not hasattr(brain_instance, "process"):
        answer = None
    else:
        answer = brain_instance.process(command)

    bus.publish("ai.response", answer)

bus.subscribe("voice.command", process)

# core/service_registry.py

class ServiceRegistry:

    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        if name not in self._services:
            raise KeyError(f"Service '{name}' not registered.")
        return self._services[name]

    def exists(self, name):
        return name in self._services

    def remove(self, name):
        if name in self._services:
            del self._services[name]

    def list_services(self):
        return sorted(self._services.keys())

    def clear(self):
        self._services.clear()

registry = ServiceRegistry()

registry.register("voice", VoiceEngine())
registry.register("brain", BrainManager())
registry.register("memory", MemoryEngine())
registry.register("dashboard", CHITTDashboard())
registry.register("plugins", PluginManager())

voice = registry.get("voice")
brain = registry.get("brain")   
if registry.exists("voice"):
    registry.get("voice").speak("CHITT is ready.")
 # core/command_pipeline.py

class CommandPipeline:

    def __init__(self, registry):

        self.registry = registry

    def execute(self, command):

        memory = self.registry.get("memory")
        brain = self.registry.get("brain")
        router = self.registry.get("router")
        voice = self.registry.get("voice")

        # Save command
        memory.set("last_command", command)

        # Process command
        result = brain.process(command)

        # Execute action
        if result.get("intent"):
            router.route(result)

        # Speak response
        response = result.get("response")

        if response:
            voice.speak(response)

        return result

class CommandRouter:

    def route(self, result):

        intent = result.get("intent")

        if intent == "open_google":
            self.open_google()

        elif intent == "open_youtube":
            self.open_youtube()

        elif intent == "play_music":
            self.play_music()

        elif intent == "shutdown":
            self.shutdown_pc()

    def open_google(self):
        import webbrowser
        webbrowser.open("https://www.google.com")

    def open_youtube(self):
        import webbrowser
        webbrowser.open("https://www.youtube.com")

    def play_music(self):
        print("Playing Music...")

    def shutdown_pc(self):
        print("Shutdown requested.")


# Initialize pipeline and start main loop
pipeline = CommandPipeline(registry)

while True:
    command = voice.listen()
    if not command:
        continue
    pipeline.execute(command)
    # core/ai_orchestrator.py

class AIOrchestrator:

    def __init__(self, registry):

        self.registry = registry

    def process(self, command):

        memory = self.registry.get("memory")
        context = self.registry.get("context")
        brain = self.registry.get("brain")
        router = self.registry.get("router")
        voice = self.registry.get("voice")

        # Store command
        context.add("User", command)
        memory.set("last_command", command)

        # AI Processing
        result = brain.process(command)

        response = result.get("response")

        # Execute action
        router.route(result)

        # Speak
        if response:
            voice.speak(response)

        # Save response
        context.add("CHITT", response)

        return result

# Register services helper
def register_services(registry):
    registry.register("voice", VoiceEngine())
    registry.register("brain", BrainManager())
    registry.register("memory", MemoryEngine())
    registry.register("context", ContextEngine())
    registry.register("router", CommandRouter())
    registry.register("dashboard", CHITTDashboard())
    registry.register("plugins", PluginManager())

# If registry exists, register services
try:
    register_services(registry)
except NameError:
    # registry not defined in this scope
    pass

# Start orchestrator loop if components available
try:
    orchestrator = AIOrchestrator(registry)
    while True:
        command = voice.listen()
        if not command:
            continue
        orchestrator.process(command)
except NameError:
    # Required components not available in this context
    pass
# core/task_scheduler.py

import threading
import queue
import time

class TaskScheduler:

    def __init__(self, workers=4):
        self.tasks = queue.Queue()
        self.running = True

        self.workers = []

        for _ in range(workers):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()
            self.workers.append(t)

    def worker(self):

        while self.running:

            try:

                func, args, kwargs = self.tasks.get(timeout=1)

                func(*args, **kwargs)

            except queue.Empty:
                continue

            except Exception as e:
                print(f"[TASK ERROR] {e}")

            finally:
                if not self.tasks.empty():
                    self.tasks.task_done()

    def submit(self, func, *args, **kwargs):

        self.tasks.put((func, args, kwargs))

    def stop(self):

        self.running = False

    def wait(self):

        self.tasks.join()
from core.task_scheduler import TaskScheduler

scheduler = TaskScheduler(workers=4)

scheduler.submit(
    voice.speak,
    "CHITT AI is Ready."
)

scheduler.submit(
    brain.process,
    "Open Google"
)       
result = brain.process(command)

scheduler.submit(
    router.route,
    result
)

scheduler.submit(
    dashboard.add_message,
    "User",
    command
)

scheduler.submit(
    dashboard.add_message,
    "CHITT",
    result.get("response", "")
)
# core/ai_kernel.py

import time

class AIKernel:

    def __init__(self, registry):

        self.registry = registry

        self.running = False

    def boot(self):

        print("[CHITT] Booting...")

        self.running = True

        voice = self.registry.get("voice")

        voice.speak("CHITT AI is starting.")

        print("[CHITT] Ready")

    def shutdown(self):

        self.running = False

        voice = self.registry.get("voice")

        voice.speak("Goodbye.")

        print("[CHITT] Shutdown")

    def execute(self, command):

        if not self.running:
            return

        orchestrator = self.registry.get("orchestrator")

        return orchestrator.process(command)

    def loop(self):

        voice = self.registry.get("voice")

        while self.running:

            command = voice.listen()

            if not command:
                continue

            self.execute(command)

            time.sleep(0.1)
            from core.ai_kernel import AIKernel

kernel = AIKernel(registry)

kernel.boot()

kernel.loop()
# core/config_manager.py

import json
import os

class ConfigManager:

    def __init__(self, filename="config.json"):
        self.filename = filename
        self.config = {}
        self.load()

    def load(self):

        if os.path.exists(self.filename):

            with open(self.filename, "r", encoding="utf-8") as f:
                self.config = json.load(f)

        else:
            self.create_default()

    def create_default(self):

        self.config = {

            "assistant_name": "CHITT",

            "language": "en",

            "voice_enabled": True,

            "wake_word": "hey chitt",

            "theme": "dark",

            "gemini_api_key": "",

            "offline_mode": False,

            "log_level": "INFO"

        }

        self.save()

    def save(self):

        with open(self.filename, "w", encoding="utf-8") as f:

            json.dump(
                self.config,
                f,
                indent=4,
                ensure_ascii=False
            )

    def get(self, key, default=None):

        return self.config.get(key, default)

    def set(self, key, value):

        self.config[key] = value

        self.save()
        # imports.py

import importlib
import traceback

def safe_import(module_name, class_name=None):
    try:
        module = importlib.import_module(module_name)

        if class_name:
            return getattr(module, class_name)

        return module

    except Exception as e:
        print(f"[IMPORT ERROR] {module_name}")
        print(e)
        traceback.print_exc()
        return None
    from imports import safe_import

CHITTCore = safe_import("ai_core", "CHITTCore")
VoiceEngine = safe_import("voice_engine", "VoiceEngine")
MemoryEngine = safe_import("memory_engine", "MemoryEngine")
BrainManager = safe_import("brain_manager", "BrainManager")
CommandRouter = safe_import("command_router", "CommandRouter")
PluginManager = safe_import("plugin_manager", "PluginManager")
CHITTDashboard = safe_import("dashboard", "CHITTDashboard")
# error_handler.py

import traceback
from datetime import datetime

class ErrorHandler:

    @staticmethod
    def log(error):

        with open("logs/errors.log", "a", encoding="utf-8") as f:

            f.write("\n")
            f.write("=" * 60)
            f.write("\n")

            f.write(str(datetime.now()))
            f.write("\n")

            f.write(str(error))
            f.write("\n")

            traceback.print_exc(file=f)

modules = [
    "ai_core",
    "voice_engine",
    "memory_engine",
    "brain_manager",
    "command_router",
    "dashboard",
    "plugin_manager"
]

for module in modules:

    if safe_import(module):

        print(f"[OK] {module}")

    else:

        print(f"[FAILED] {module}")
        # logger.py

import logging
import os

class Logger:

    @staticmethod
    def setup():

        os.makedirs("logs", exist_ok=True)

        logging.basicConfig(
            filename="logs/chitt.log",
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            encoding="utf-8"
        )

    @staticmethod
    def info(message):
        logging.info(message)
        print("[INFO]", message)

    @staticmethod
    def warning(message):
        logging.warning(message)
        print("[WARNING]", message)

    @staticmethod
    def error(message):
        logging.error(message)
        print("[ERROR]", message)

    @staticmethod
    def exception(error):
        logging.exception(error)
        print("[EXCEPTION]", error)
from logger import Logger

Logger.setup()

Logger.info("Starting CHITT AI...")        
try:

    Logger.info("Voice Engine Started")

    command = voice.listen()

    Logger.info(f"User: {command}")

    result = brain.process(command)

    Logger.info(f"AI: {result}")

    voice.speak(result["response"])

except Exception as e:

    Logger.exception(e)
 # module_manager.py

class ModuleManager:

    def __init__(self):
        self.modules = {}

    def register(self, name, module):
        self.modules[name] = module
        print(f"[MODULE] Registered: {name}")

    def get(self, name):
        return self.modules.get(name)

    def start_all(self):
        for name, module in self.modules.items():
            if hasattr(module, "start"):
                try:
                    module.start()
                    print(f"[STARTED] {name}")
                except Exception as e:
                    print(f"[ERROR] {name}: {e}")

    def stop_all(self):
        for name, module in self.modules.items():
            if hasattr(module, "stop"):
                try:
                    module.stop()
                    print(f"[STOPPED] {name}")
                except Exception as e:
                    print(f"[ERROR] {name}: {e}")

    def list_modules(self):
        return list(self.modules.keys())
from module_manager import ModuleManager

manager = ModuleManager()

manager.register("Voice", voice)
manager.register("Brain", brain)
manager.register("Memory", memory)
manager.register("Dashboard", dashboard)
manager.register("Plugins", plugins)

manager.start_all()

print(manager.list_modules())
# core/system_initializer.py

from logger import Logger

class SystemInitializer:

    def __init__(self, registry):

        self.registry = registry

    def initialize(self):

        Logger.info("Initializing CHITT AI...")

        startup_order = [
            "config",
            "memory",
            "knowledge",
            "context",
            "voice",
            "brain",
            "router",
            "dashboard",
            "plugins"
        ]

        for service in startup_order:

            if not self.registry.exists(service):
                Logger.warning(f"{service} not found")
                continue

            obj = self.registry.get(service)

            if hasattr(obj, "initialize"):
                try:
                    obj.initialize()
                    Logger.info(f"{service} initialized")
                except Exception as e:
                    Logger.error(f"{service}: {e}")

        Logger.info("CHITT AI Ready")
        from core.system_initializer import SystemInitializer

initializer = SystemInitializer(registry)

initializer.initialize()

kernel.boot()

kernel.loop()
class Config:

    APP_NAME = "CHITT AI"

    VERSION = "1.0"

    AUTHOR = "Manoj"

    DEBUG = True

    OFFLINE_MODE = False

    LANGUAGE = "hi"

    WAKE_WORD = "hey chitt"
    # core/dependency_checker.py

import importlib
import os

class DependencyChecker:

    REQUIRED_MODULES = [
        "speech_recognition",
        "pyttsx3",
        "pygame",
        "google.generativeai",
        "deep_translator",
        "langdetect",
        "psutil",
        "requests"
    ]

    REQUIRED_FOLDERS = [
        "logs",
        "memory",
        "plugins",
        "data",
        "models"
    ]

    def check_modules(self):

        missing = []

        for module in self.REQUIRED_MODULES:

            try:
                importlib.import_module(module)

                print(f"[OK] {module}")

            except ImportError:

                print(f"[MISSING] {module}")

                missing.append(module)

        return missing

    def check_folders(self):

        for folder in self.REQUIRED_FOLDERS:

            os.makedirs(folder, exist_ok=True)

            print(f"[READY] {folder}")

    def run(self):

        self.check_folders()

        missing = self.check_modules()

        if missing:

            print("\nInstall missing packages:")

            for module in missing:

                print(f"pip install {module}")

            return False

        print("\nAll dependencies are ready.")

        return True
    from core.dependency_checker import DependencyChecker

checker = DependencyChecker()

if not checker.run():

    exit()

print("Starting CHITT AI...")
# core/health_manager.py

import time

class HealthManager:

    def __init__(self, registry):
        self.registry = registry
        self.status = {}

    def check_service(self, name):

        try:
            service = self.registry.get(name)

            if hasattr(service, "health"):
                self.status[name] = service.health()
            else:
                self.status[name] = "OK"

        except Exception as e:
            self.status[name] = f"ERROR: {e}"

    def check_all(self):

        for name in self.registry.list_services():
            self.check_service(name)

        return self.status

    def print_report(self):

        print("\n===== CHITT Health Report =====")

        for name, state in self.status.items():
            print(f"{name:20} : {state}")

        print("=" * 35)

    def monitor(self, interval=10):

        while True:

            self.check_all()

            self.print_report()

            time.sleep(interval)
        # end monitor

# Example usage (ensure 'registry' is defined in this module)
try:
    from core.health_manager import HealthManager

    health = HealthManager(registry)
    health.check_all()
    health.print_report()
except Exception:
    # If registry is not available or import fails, skip example usage
    pass
# core/service_monitor.py

import threading
import time

class ServiceMonitor:

    def __init__(self, registry, interval=5):
        self.registry = registry
        self.interval = interval
        self.running = False

    def check_service(self, name, service):

        try:

            if hasattr(service, "health"):

                state = service.health()

                if state != "Running":

                    print(f"[WARNING] {name}: {state}")

                    if hasattr(service, "start"):

                        print(f"[RECOVERY] Restarting {name}")

                        service.start()

            else:

                print(f"[OK] {name}")

        except Exception as e:

            print(f"[ERROR] {name}: {e}")

    def monitor_loop(self):

        while self.running:

            for name in self.registry.list_services():

                service = self.registry.get(name)

                self.check_service(name, service)

            time.sleep(self.interval)

    def start(self):

        if self.running:
            return

        self.running = True

        thread = threading.Thread(
            target=self.monitor_loop,
            daemon=True
        )

        thread.start()

    def stop(self):

        self.running = False
        from core.service_monitor import ServiceMonitor

monitor = ServiceMonitor(registry)

monitor.start()
# core/performance_monitor.py

import psutil
import time
from logger import Logger

class PerformanceMonitor:

    def __init__(self):
        self.start_time = time.time()

    def cpu_usage(self):
        return psutil.cpu_percent(interval=0.5)

    def memory_usage(self):
        mem = psutil.virtual_memory()
        return {
            "percent": mem.percent,
            "used_gb": round(mem.used / (1024**3), 2),
            "total_gb": round(mem.total / (1024**3), 2)
        }

    def uptime(self):
        seconds = int(time.time() - self.start_time)
        return seconds

    def report(self):

        cpu = self.cpu_usage()
        memory = self.memory_usage()

        Logger.info(f"CPU Usage: {cpu}%")
        Logger.info(
            f"RAM: {memory['used_gb']}GB / {memory['total_gb']}GB "
            f"({memory['percent']}%)"
        )
        Logger.info(f"Uptime: {self.uptime()} seconds")

        return {
            "cpu": cpu,
            "memory": memory,
            "uptime": self.uptime()
        }

# instantiate performance monitor and update dashboard
from core.performance_monitor import PerformanceMonitor

performance = PerformanceMonitor()
status = performance.report()

print(status)

dashboard.update_cpu(status["cpu"])
dashboard.update_memory(status["memory"]["percent"])
dashboard.update_uptime(status["uptime"])
# core/startup_manager.py

from logger import Logger

class StartupManager:

    def __init__(self, registry):
        self.registry = registry

    def start(self):

        startup_order = [
            "config",
            "logger",
            "memory",
            "knowledge",
            "context",
            "voice",
            "brain",
            "router",
            "dashboard",
            "plugins",
            "scheduler",
            "performance",
            "health"
        ]

        Logger.info("Starting CHITT AI...")

        for service_name in startup_order:

            if not self.registry.exists(service_name):
                Logger.warning(f"{service_name} not registered")
                continue

            service = self.registry.get(service_name)

            try:

                if hasattr(service, "start"):
                    service.start()

                Logger.info(f"{service_name} started")

            except Exception as e:

                Logger.error(f"{service_name}: {e}")

        Logger.info("CHITT AI Startup Complete")


if __name__ == "__main__":
    from core.startup_manager import StartupManager

    startup = StartupManager(registry)
    startup.start()

    kernel.boot()
    kernel.loop()
 # core/message_bus.py

import threading
from queue import Queue, Empty

class MessageBus:

    def __init__(self):
        self.queue = Queue()
        self.subscribers = {}
        self.running = False

    def subscribe(self, topic, callback):

        if topic not in self.subscribers:
            self.subscribers[topic] = []

        self.subscribers[topic].append(callback)

    def publish(self, topic, data=None):

        self.queue.put((topic, data))

    def start(self):

        self.running = True

        threading.Thread(
            target=self._worker,
            daemon=True
        ).start()

    def stop(self):

        self.running = False

    def _worker(self):

        while self.running:

            try:

                topic, data = self.queue.get(timeout=1)

                if topic in self.subscribers:

                    for callback in self.subscribers[topic]:

                        try:

                            callback(data)

                        except Exception as e:

                            print(f"[MESSAGE BUS] {e}")

                self.queue.task_done()

            except Empty:

                pass

from core.message_bus import MessageBus

bus = MessageBus()

bus.start()

def on_voice(command):
    print(command)

bus.subscribe("voice.command", on_voice)

bus.publish(
    "voice.command",
    "Open Google"
)

def process(command):
    answer = brain.process(command)

    bus.publish(
        "ai.response",
        answer
    )

bus.subscribe(
    "voice.command",
    process
)

def update(data):
    dashboard.add_message(
        "CHITT",
        data["response"]
    )

bus.subscribe(
    "ai.response",
    update
)
# core/command_history.py

import json
import os
from datetime import datetime

class CommandHistory:

    def __init__(self, file_name="data/history.json"):
        self.file_name = file_name

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file_name):
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add(self, command, response):

        with open(self.file_name, "r", encoding="utf-8") as f:
            history = json.load(f)

        history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "command": command,
            "response": response
        })

        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def get_all(self):

        with open(self.file_name, "r", encoding="utf-8") as f:
            return json.load(f)

    def last(self):

        history = self.get_all()

        if history:
            return history[-1]

        return None

    def clear(self):

        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump([], f)
from core.command_history import CommandHistory

history = CommandHistory()

command = voice.listen()

result = brain.process(command)

history.add(
    command,
    result["response"]
)

voice.speak(result["response"])
last = history.last()

print(last)

for item in history.get_all():

    print(item["time"])
    print(item["command"])
    print(item["response"])           
  # core/cache_manager.py

import json
import hashlib
import os
from datetime import datetime

class CacheManager:

    def __init__(self, filename="data/cache.json"):

        self.filename = filename

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump({}, f)

        self.load()

    def load(self):

        with open(self.filename, "r", encoding="utf-8") as f:
            self.cache = json.load(f)

    def save(self):

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(
                self.cache,
                f,
                indent=4,
                ensure_ascii=False
            )

    def _key(self, text):

        return hashlib.sha256(
            text.lower().encode("utf-8")
        ).hexdigest()

    def get(self, text):

        key = self._key(text)

        return self.cache.get(key)

    def set(self, text, answer):

        key = self._key(text)

        self.cache[key] = {

            "question": text,

            "answer": answer,

            "time": str(datetime.now())

        }

        self.save()

    def clear(self):

        self.cache = {}

        self.save()

    def size(self):

        return len(self.cache)
cache = CacheManager()

answer = cache.get(command)

if answer:

    voice.speak(answer["answer"])

else:

    answer = ask_gemini(command)

    cache.set(command, answer)

    voice.speak(answer)
cache.set(
    "what is python",
    "Python is a programming language."
)

print(
    cache.get("what is python")
)

print(
    cache.size()
)
# core/command_dispatcher.py

from logger import Logger

class CommandDispatcher:

    def __init__(self, registry):
        self.registry = registry

    def dispatch(self, command):

        brain = self.registry.get("brain")
        router = self.registry.get("router")
        memory = self.registry.get("memory")
        history = self.registry.get("history")
        cache = self.registry.get("cache")

        Logger.info(f"Command: {command}")

        # Cache Check
        cached = cache.get(command)

        if cached:

            Logger.info("Response from Cache")

            history.add(command, cached["answer"])

            return cached["answer"]

        # AI Processing
        result = brain.process(command)

        response = result.get(
            "response",
            "Sorry, I don't know."
        )

        # Save
        memory.set("last_command", command)

        history.add(command, response)

        cache.set(command, response)

        # Execute Action
        router.route(result)

        return response
dispatcher = CommandDispatcher(registry)

while True:

    command = voice.listen()

    if not command:
        continue

    response = dispatcher.dispatch(command)

    voice.speak(response)    
# core/response_generator.py

from logger import Logger

class ResponseGenerator:

    def __init__(self, registry):
        self.registry = registry

    def generate(self, command):

        cache = self.registry.get("cache")
        brain = self.registry.get("brain")
        history = self.registry.get("history")
        memory = self.registry.get("memory")

        # Check Cache
        cached = cache.get(command)

        if cached:
            Logger.info("Cache Hit")
            return cached["answer"]

        # Process with Brain
        result = brain.process(command)

        response = result.get(
            "response",
            "Sorry, I don't understand."
        )

        # Save
        cache.set(command, response)
        history.add(command, response)
        memory.set("last_response", response)

        return response
response_generator = ResponseGenerator(registry)

while True:

    command = voice.listen()

    if not command:
        continue

    response = response_generator.generate(command)

    voice.speak(response)
dashboard.add_message(
    "User",
    command
)

dashboard.add_message(
    "CHITT",
    response
)
def main():

    # Logger
    logger.setup()

    # Config
    config.load()

    # Registry
    registry = ServiceRegistry()

    # Register Services
    register_all(registry)

    # Initialize
    initializer.initialize()

    # Start Voice
    voice.start()

    # Main Loop
    while True:

        command = voice.listen()

        if not command:
            continue

        result = brain.process(command)

        router.route(result)

        voice.speak(result["response"])
# core/bootstrap.py

from logger import Logger

class Bootstrap:

    def __init__(self, registry):
        self.registry = registry

    def boot(self):

        Logger.info("===== CHITT AI Boot =====")

        for name in self.registry.list_services():

            service = self.registry.get(name)

            if hasattr(service, "initialize"):
                service.initialize()

            elif hasattr(service, "start"):
                service.start()

            Logger.info(f"{name} Ready")

        Logger.info("===== CHITT Ready =====")
from core.bootstrap import Bootstrap

bootstrap = Bootstrap(registry)

bootstrap.boot()

kernel.loop()
# core/brain.py

class Brain:

    def __init__(self):

        self.online = False

        self.memory = None
        self.router = None
        self.chat_ai = None

    def initialize(
            self,
            memory,
            router,
            chat_ai):

        self.memory = memory
        self.router = router
        self.chat_ai = chat_ai

    def process(self, command):

        command = command.strip()

        # Save command
        self.memory.save_command(command)

        # Offline command first
        result = self.router.execute(command)

        if result["success"]:

            self.memory.save_response(
                result["response"]
            )

            return result

        # Online AI
        if self.online:

            answer = self.chat_ai.ask(command)

            self.memory.save_response(answer)

            return {

                "success": True,

                "response": answer,

                "source": "online"

            }

        return {

            "success": False,

            "response": "Sorry, I can't understand this command.",

            "source": "offline"

        }

    def set_online(self, state):

        self.online = state
brain = Brain()

brain.initialize(

    memory,

    router,

    chat_ai

)

while True:

    command = voice.listen()

    result = brain.process(command)

    voice.speak(result["response"])
     

    

