"""
CHITT Text To Speech Engine
"""

import pyttsx3

from .config import (
    PERSONALITIES,
    DEFAULT_PERSONA,
)


class TextToSpeech:

    def __init__(self, persona=DEFAULT_PERSONA):

        self.engine = pyttsx3.init()

        self.persona = persona

        self.voice_config = PERSONALITIES[self.persona]

        self.configure()

    def configure(self):

        self.engine.setProperty(
            "rate",
            int(180 * self.voice_config["speed"])
        )

        self.engine.setProperty(
            "volume",
            1.0
        )

        voices = self.engine.getProperty("voices")

        gender = self.voice_config["gender"]

        for voice in voices:

            name = voice.name.lower()

            if gender == "female":

                if "female" in name or "zira" in name:

                    self.engine.setProperty(
                        "voice",
                        voice.id
                    )

                    break

            else:

                if (
                    "male" in name
                    or "david" in name
                    or "mark" in name
                ):

                    self.engine.setProperty(
                        "voice",
                        voice.id
                    )

                    break

    def speak(self, text):

        print(f"{self.persona} : {text}")

        self.engine.say(text)

        self.engine.runAndWait()


if __name__ == "__main__":

    aura = TextToSpeech("Aura")

    aura.speak(
        "Hello Avishkar. Welcome back."
    )

    nova = TextToSpeech("Nova")

    nova.speak(
        "All systems are online."
    )
    