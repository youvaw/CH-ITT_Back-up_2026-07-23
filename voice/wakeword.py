"""
=========================================
CHITT - Wake Word
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.2.0
=========================================
"""

import speech_recognition as sr
from thefuzz import fuzz


class WakeWord:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.microphone = sr.Microphone(
            device_index=1
        )

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

        self.fuzzy_threshold = 65

    # ---------------------------------
    # Add Wake Word
    # ---------------------------------

    def add(self, wake_word):

        wake_word = wake_word.lower().strip()

        if wake_word not in self.wake_words:

            self.wake_words.append(wake_word)

    # ---------------------------------
    # Remove Wake Word
    # ---------------------------------

    def remove(self, wake_word):

        wake_word = wake_word.lower().strip()

        if wake_word in self.wake_words:

            self.wake_words.remove(wake_word)

    # ---------------------------------
    # Get Wake Words
    # ---------------------------------

    def get_all(self):

        return self.wake_words

    # ---------------------------------
    # Check Wake Word
    # ---------------------------------

    def is_wake_word(self, text):

        if not text:

            return False

        text = text.lower().strip()

        # Direct match
        for wake in self.wake_words:

            if wake in text:

                print(
                    f"Wake Word Detected: {wake}"
                )

                return True

        # Fuzzy match
        for wake in self.wake_words:

            similarity = fuzz.partial_ratio(
                wake,
                text
            )

            if similarity >= self.fuzzy_threshold:

                print(
                    f"[+] Fuzzy Match: "
                    f"{similarity}% | "
                    f"'{text}' -> '{wake}'"
                )

                print("Wake Word Detected!")

                return True

        return False

    # ---------------------------------
    # Listen
    # ---------------------------------

    def detect(self):

        try:

            with self.microphone as source:

                print(
                    "Waiting for Wake Word..."
                )

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            print("Recognizing...")

            text = self.recognizer.recognize_google(  # type: ignore[attr-defined]
                audio,
                language=self.language
            )

            print("Heard :", text)

            return self.is_wake_word(text)

        except sr.WaitTimeoutError:

            return False

        except sr.UnknownValueError:

            return False

        except sr.RequestError as error:

            print(
                "Speech service error:",
                error
            )

            return False

        except KeyboardInterrupt:

            print(
                "\nWake Word Listener Stopped."
            )

            return False

        except Exception as error:

            print(
                "Wake Word Error:",
                error
            )

            return False

    # ---------------------------------
    # Language
    # ---------------------------------

    def set_language(self, language):

        self.language = language

    def get_language(self):

        return self.language


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    wake = WakeWord()

    print("CHITT Wake Word Test")
    print("Say: चिट्टी / चिती / हॅलो / CHITT")
    print("Press Ctrl+C to stop.")

    while True:

        if wake.detect():

            print(
                "CHITT Activated!"
            )

            break

import speech_recognition as sr

class WakeWordListener:
    def __init__(self, wake_word="mayax"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()

    def listen_for_wakeword(self, callback_function):
        """
        बॅकग्राऊंडमध्ये सतत ऐकून 'MAYAX' हा शब्द शोधणे
        """
        with sr.Microphone() as source:
            print("👂 Wake Word Listener Active (Listening for 'MAYAX')...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=4)
                    text = self.recognizer.recognize_google(audio, language="en-US").lower()
                    print(f"Detected: {text}")

                    if self.wake_word in text:
                        print("⚡ Wake Word Detected!")
                        callback_function() # Wake word भेटल्यावर हे फंक्शन रन होईल
                except (sr.WaitTimeoutError, sr.UnknownValueError):
                    pass
                except Exception as e:
                    print(f"WakeWord Error: {e}")
                        