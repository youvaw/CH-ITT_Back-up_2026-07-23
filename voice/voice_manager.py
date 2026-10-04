# -*- coding: utf-8 -*-

import time

from voice.speech_to_text import SpeechToText
from voice.text_to_speech import MyXTTS


class VoiceManager:

    def __init__(self):

        print("[VoiceManager] Initializing...")

        # Speech To Text
        try:
            self.stt = SpeechToText(
                model_size="base",
                sample_rate=48000,
                device=9,
                record_seconds=5
            )
            print("[VoiceManager] STT Connected Successfully!")
        except Exception as e:
            print(f"[VoiceManager] STT Error: {e}")
            self.stt = None

        # Text To Speech
        try:
            self.tts = MyXTTS()
            print("[VoiceManager] TTS Connected Successfully!")
        except Exception as e:
            print(f"[VoiceManager] TTS Error: {e}")
            self.tts = None

        # Wake Word Setup
        self.wakeword = None
        self.has_wakeword = False

        try:
            from voice.wakewordlistener import WakeWordListener

            self.wakeword = WakeWordListener()
            self.has_wakeword = True

            print("[VoiceManager] Wake Word Connected Successfully!")

        except Exception as e:

            print(f"[Warning] Wake word unavailable: {e}")
            print("[VoiceManager] Continuing without Wake Word...")

        # Brain Setup
        self.brain = None

        try:

            from src.core.brain import Brain

            self.brain = Brain()

            print("[VoiceManager] Brain Module Connected Successfully!")

        except Exception as e:

            print(f"[Warning] Brain load failed: {e}")


    def process_command(self):

        print("\n[VoiceManager] Triggered!")

        time.sleep(0.3)

        if self.stt is None:

            print("[VoiceManager] STT is unavailable.")
            return

        # Listen
        command_text = self.stt.listen()

        if not command_text:

            msg = "I didn't hear anything."

            print(f"[VoiceManager] CHITT Response: {msg}")

            if self.tts:
                self.tts.speak(msg)

            return

        print(f"[VoiceManager] User Said: {command_text}")

        # Brain
        if self.brain:

            try:

                response_text = self.brain.process(command_text)

            except Exception as e:

                response_text = f"Brain error: {e}"

        else:

            response_text = f"You said: {command_text}"

        print(f"[VoiceManager] CHITT Response: {response_text}")

        # Speak
        if self.tts:

            self.tts.speak(response_text)


    def start(self):

        print("\n==========================================")
        print("          CHITT VOICE MANAGER")
        print("==========================================")

        if self.has_wakeword:

            print("[VoiceManager] CHITT Active.")
            print("[VoiceManager] Listening for Wake Word...")

            try:

                self.wakeword.start_listening(
                    self.process_command
                )

            except Exception as e:

                print(f"[WakeWord ERROR] {e}")

        else:

            print("[VoiceManager] Direct Voice Mode Active.")

            if self.tts:

                self.tts.speak(
                    "Hello Avishkar. I am CHITT. "
                    "Voice mode is ready."
                )

            self.process_command()


if __name__ == "__main__":

    manager = VoiceManager()

    manager.start()
    
