import pyttsx3


class MyXTTS:

    def __init__(self):

        print("[TTS] Initializing...")

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

        voices = self.engine.getProperty("voices")

        if voices:
            self.engine.setProperty(
                "voice",
                voices[0].id
            )

        print("[TTS] Engine Ready")

    def speak(self, text):

        text = str(text).strip()

        if not text:
            return

        print(f"[MYX Speaking] {text}")

        try:
            self.engine.say(text)
            self.engine.runAndWait()

        except Exception as e:
            print(f"[TTS ERROR] {e}")

    def stop(self):

        try:
            self.engine.stop()
        except Exception:
            pass


if __name__ == "__main__":

    print("==========================================")
    print("          MYX TTS TEST")
    print("==========================================")

    tts = MyXTTS()

    tts.speak(
        "Hello Avishkar. I am MYX. "
        "Your local voice assistant is ready."
    )

    print()
    print("[TTS] Test completed.")

