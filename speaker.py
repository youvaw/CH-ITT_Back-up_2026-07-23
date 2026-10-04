"""
=========================================
CHITT - Speaker
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import pyttsx3


class Speaker:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.volume = 1.0

        self.rate = 180

        self.engine.setProperty(

            "volume",

            self.volume

        )

        self.engine.setProperty(

            "rate",

            self.rate

        )

    # ---------------------------------
    # Speak
    # ---------------------------------

    def speak(self, text):

        if not text:

            return

        self.engine.say(str(text))

        self.engine.runAndWait()

    # ---------------------------------
    # Stop Speaker
    # ---------------------------------

    def stop(self):

        self.engine.stop()

    # ---------------------------------
    # Pause
    # ---------------------------------

    def pause(self):

        self.engine.stop()

    # ---------------------------------
    # Resume
    # ---------------------------------

    def resume(self):

        pass

    # ---------------------------------
    # Volume
    # ---------------------------------

    def set_volume(self, volume):

        self.volume = volume

        self.engine.setProperty(

            "volume",

            volume

        )

    def get_volume(self):

        return self.volume

    # ---------------------------------
    # Speed
    # ---------------------------------

    def set_rate(self, rate):

        self.rate = rate

        self.engine.setProperty(

            "rate",

            rate

        )

    def get_rate(self):

        return self.rate

    # ---------------------------------
    # Voice
    # ---------------------------------

    def set_voice(self, index=0):

        voices = self.engine.getProperty(

            "voices"

        )

        if len(voices) > index:

            self.engine.setProperty(

                "voice",

                voices[index].id

            )

    # ---------------------------------
    # Test Speaker
    # ---------------------------------

    def test(self):

        self.speak(

            "Speaker test completed successfully."

        )


if __name__ == "__main__":

    speaker = Speaker()

    speaker.test()
    