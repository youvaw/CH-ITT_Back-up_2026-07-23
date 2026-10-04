"""
=========================================
CHITT - Wake Word
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.1.0 (with Fuzzy Matching)
=========================================
"""

import speech_recognition as sr
from thefuzz import fuzz


class WakeWord:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=1)
        self.wake_words = [
            "chitt",
            "hey chitt",
            "hello chitt",
            "चिट्टी",
            "हे चिट्टी",
            "हॅलो चिट्टी",
            "चिती",
            "किती",
            "हॅलो"
        ]
        self.language = "mr-IN"

    def add(self, wake_word):
        wake_word = wake_word.lower()
        if wake_word not in self.wake_words:
            self.wake_words.append(wake_word)

    def remove(self, wake_word):
        wake_word = wake_word.lower()
        if wake_word in self.wake_words:
            self.wake_words.remove(wake_word)

    def get_all(self):
        return self.wake_words

    def detect(self):
        try:
            with self.microphone as source:
                print("Waiting for Wake Word...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)

            text = self.recognizer.recognize_google(
                audio,
                language=self.language
            ).lower()
            print("Heard :", text)

            # 1. Direct Keyword Check
            for wake in self.wake_words:
                if wake in text:
                    print("Wake Word Detected!")
                    return True

            # 2. Fuzzy Matching Check (उच्चारात चूक झाल्यास)
            for wake in self.wake_words:
                similarity = fuzz.partial_ratio(wake, text)
                if similarity >= 65:
                    print(f"[+] Fuzzy Match Found ({similarity}%): '{text}' -> '{wake}'")
                    print("Wake Word Detected!")
                    return True

            return False

        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except sr.RequestError:
            return False
        except Exception as error:
            print(f"Error: {error}")
            return False

    def set_language(self, language):
        self.language = language

    def get_language(self):
        return self.language


if __name__ == "__main__":
    wake = WakeWord()
    while True:
        try:
            if wake.detect():
                print("CHITT Activated!")
                break
        except KeyboardInterrupt:
            print("\n[+] Wake Word Listener Stopped.")
            break
        from voice.wakeword import WakeWord

wake = WakeWord()
if wake.detect():
    # तुमची मुख्य AI कमांड लिसनिंग लॉजिक येथे सुरू करा
    pass
import pvporcupine
from pvrecorder import PvRecorder

class OfflineWakeWord:
    def __init__(self, sensitivity=0.7):
        # Inbuilt lightweight wake words (उदा. Jarvis, Porcupine, Picovoice, Alexa)
        # Custom "Chitt" साठी Picovoice Console वरून .ppn फाईल डाउनलोड करून path वापरता येतो.
        self.keywords = ["jarvis", "porcupine"]
        self.porcupine = pvporcupine.create(keywords=self.keywords, sensitivities=[sensitivity]*len(self.keywords))
        
        # device_index=1 (Lenovo LOQ Microphone)
        self.recorder = PvRecorder(device_index=1, frame_length=self.porcupine.frame_length)

    def listen_for_wake_word(self):
        print("Waiting for Wake Word (Offline Mode)...")
        self.recorder.start()
        
        try:
            while True:
                pcm = self.recorder.read()
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    detected = self.keywords[keyword_index]
                    print(f"\n[+] Wake Word Detected: '{detected.upper()}'")
                    return True
        except KeyboardInterrupt:
            print("\nStopped.")
            return False
        finally:
            self.recorder.stop()

    def close(self):
        self.recorder.delete()
        self.porcupine.delete()

if __name__ == "__main__":
    detector = OfflineWakeWord()
    if detector.listen_for_wake_word():
        print("CHITT Activated via Offline Engine!")
    detector.close()