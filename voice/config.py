"""
CHITT Voice Configuration
"""

from pathlib import Path


# ===========================================
# Assistant
# ===========================================

ASSISTANT_NAME = "CHITT"

DEFAULT_PERSONA = "Aura"

DEFAULT_LANGUAGE = "hi-IN"


# ===========================================
# Personalities
# ===========================================

PERSONALITIES = {

    "Aura": {
        "gender": "female",
        "voice_style": "premium",
        "emotion": True,
        "speed": 1.0,
        "pitch": 1.0,
    },

    "Nova": {
        "gender": "male",
        "voice_style": "cinematic",
        "emotion": True,
        "speed": 0.95,
        "pitch": 0.90,
    }

}


# ===========================================
# Supported Languages
# ===========================================

LANGUAGES = {

    "en": "English",

    "hi": "Hindi",

    "mr": "Marathi",

    "hinglish": "Hinglish",

    "mix": "Auto"

}


AUTO_LANGUAGE = True


# ===========================================
# Wake Words
# ===========================================

WAKE_WORDS = [

    "hey chitt",

    "hello chitt",

    "chitt",

    "aura",

    "nova"

]


# ===========================================
# Voice Settings
# ===========================================

LISTEN_TIMEOUT = 5

PHRASE_TIMEOUT = 3

ENERGY_THRESHOLD = 300

PAUSE_THRESHOLD = 0.8


# ===========================================
# Audio
# ===========================================

AUDIO_FOLDER = Path("voice")

AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)


VOICE_CACHE = AUDIO_FOLDER / "cache"

VOICE_CACHE.mkdir(parents=True, exist_ok=True)


# ===========================================
# Startup Message
# ===========================================

STARTUP_MESSAGE = {

    "Aura":
    "Hello Avishkar. Welcome back. I am ready. What shall we build today?",

    "Nova":
    "Welcome back Avishkar. All systems are online. Awaiting your command."

}
"""
=========================================
CHITT - Voice Configuration
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

VOICE_CONFIG = {

    # ---------------------------------
    # General
    # ---------------------------------

    "enabled": True,

    "language": "en-US",

    "voice": "default",

    "volume": 1.0,

    "rate": 180,

    # ---------------------------------
    # Wake Word
    # ---------------------------------

    "wake_word": "chitt",

    "wake_word_enabled": True,

    # ---------------------------------
    # Microphone
    # ---------------------------------

    "microphone": "default",

    "sample_rate": 16000,

    "channels": 1,

    "chunk_size": 1024,

    "noise_reduction": True,

    "ambient_duration": 1,

    # ---------------------------------
    # Speech To Text
    # ---------------------------------

    "stt_engine": "google",

    "stt_timeout": 5,

    # ---------------------------------
    # Text To Speech
    # ---------------------------------

    "tts_engine": "pyttsx3",

    "tts_enabled": True,

    # ---------------------------------
    # Speaker
    # ---------------------------------

    "speaker": "default",

    # ---------------------------------
    # Logging
    # ---------------------------------

    "debug": False,

    "log_voice": True,

    # ---------------------------------
    # Auto Start
    # ---------------------------------

    "auto_start": True,

    "continuous_listening": True

}


def get_default_config():

    """
    Return default voice configuration.
    """

    return VOICE_CONFIG.copy()


if __name__ == "__main__":

    from pprint import pprint

    pprint(get_default_config())
    