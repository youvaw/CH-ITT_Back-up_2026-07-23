import os
import time
import io
import wave
import numpy as np
import sounddevice as sd
from openwakeword.model import Model
import speech_recognition as sr

class CHITTVoiceController:
    def __init__(self, custom_model_path="models/hey_chitt.onnx", score_threshold=0.4):
        self.sample_rate = 16000
        self.command_seconds = 5
        self.score_threshold = score_threshold
        self.is_listening_command = False
        self.is_running = False

        self.recognizer = sr.Recognizer()

        print("[CHITT Voice] Loading Wake-Word Engine...")
        if os.path.exists(custom_model_path):
            self.wake_model = Model(
                wakeword_models=[custom_model_path],
                inference_framework="onnx"
            )
            self.wakeword_key = os.path.splitext(os.path.basename(custom_model_path))[0]
            print(f"[CHITT Voice] Loaded custom model: {self.wakeword_key}")
        else:
            print(f"[CHITT Voice Warning] Custom model not found. Falling back to 'hey_jarvis'...")
            self.wake_model = Model(
                wakeword_models=["hey_jarvis"],
                inference_framework="onnx"
            )
            self.wakeword_key = "hey_jarvis"

    def _transcribe_google_multi(self, audio_data_int16):
        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data_int16.tobytes())
        wav_io.seek(0)

        try:
            with sr.AudioFile(wav_io) as source:
                audio = self.recognizer.record(source)

            for lang in ("en-IN", "hi-IN", "mr-IN"):
                try:
                    text = self.recognizer.recognize_google(audio, language=lang)
                    if text:
                        print(f"[Speech Detected ({lang})]: '{text}'")
                        return text
                except Exception:
                    pass
        except Exception as e:
            print(f"[STT Error]: {e}")
        
        return ""

    def _handle_wake_detection(self, command_callback):
        self.is_listening_command = True
        print("\n[CHITT] >>> Wake Word Detected! Listening for command... <<<")

        command_audio = sd.rec(
            int(self.sample_rate * self.command_seconds),
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            device=1
        )
        sd.wait()

        print("[CHITT] Processing speech (Multi-Language STT)...")
        user_text = self._transcribe_google_multi(command_audio)

        if user_text and command_callback:
            command_callback(user_text)

        print("\n[CHITT] Resuming wake-word detection...")
        self.is_listening_command = False

    def _audio_callback(self, indata, frames, time_info, status, command_callback):
        if self.is_listening_command:
            return

        audio_int16 = (indata[:, 0] * 32767).astype(np.int16)
        scores = self.wake_model.predict(audio_int16)
        score = scores.get(self.wakeword_key, 0.0)

        if score >= self.score_threshold:
            sd.sleep(50)
            self._handle_wake_detection(command_callback)

    def start_listening(self, command_callback):
        self.is_running = True
        print("[CHITT Voice] Multi-Language Voice Controller Active...")
        print("[CHITT Voice] Say 'HEY JARVIS'...")
        
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                blocksize=1280,
                device=1,
                callback=lambda indata, frames, time, status: self._audio_callback(
                    indata, frames, time, status, command_callback
                )
            ):
                while self.is_running:
                    time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n[CHITT Voice] Stopped by user.")
        except Exception as e:
            print(f"\n[CHITT Voice Error]: {e}")

    def stop(self):
        self.is_running = False
