"""
CHITT Voice Manager
"""

from .speech_to_text import SpeechToText
from .text_to_speech import TextToSpeech


class VoiceManager:

    def __init__(self):

        self.stt = SpeechToText()

        self.tts = TextToSpeech()

    def listen(self):

        return self.stt.listen()

    def speak(self, text):

        self.tts.speak(text)

        