# -*- coding: utf-8 -*-

import numpy as np
import pyaudio
from openwakeword.model import Model


class WakeWordListener:

    def __init__(self, model_name="hey_jarvis", threshold=0.3):

        print("[WakeWord] Initializing...")

        self.threshold = threshold

        self.oww_model = Model(
            wakeword_models=[model_name],
            inference_framework="onnx"
        )

        self.audio = pyaudio.PyAudio()

        print("[WakeWord] Model Ready")


    def start_listening(self, callback):

        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1280
        )

        print("[WakeWord] Engine Active.")
        print("[WakeWord] Say 'Hey Jarvis'...")


        try:

            while True:

                data = stream.read(
                    1280,
                    exception_on_overflow=False
                )

                audio_frame = np.frombuffer(
                    data,
                    dtype=np.int16
                )

                self.oww_model.predict(audio_frame)


                for model, scores in self.oww_model.prediction_buffer.items():

                    current_score = scores[-1]


                    if current_score > 0.1:

                        print(
                            f"\r[Listening...] Score: {current_score:.2f}",
                            end=""
                        )


                    if current_score > self.threshold:

                        print(
                            f"\n\n[WakeWord] Triggered! "
                            f"({model}: {current_score:.2f})"
                        )

                        self.oww_model.reset()

                        callback()

                        break


        except KeyboardInterrupt:

            print("\n[WakeWord] Stopped.")


        finally:

            stream.stop_stream()
            stream.close()
            self.audio.terminate()


if __name__ == "__main__":

    listener = WakeWordListener()

    print("[WakeWord] Test mode started.")

    listener.start_listening(
        lambda: print("[WakeWord] CALLBACK TRIGGERED!")
    )
    