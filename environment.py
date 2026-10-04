"""
CHITT AI
Environment Configuration
"""

from enum import Enum


class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


CURRENT_ENVIRONMENT = Environment.DEVELOPMENT


def is_development() -> bool:
    return CURRENT_ENVIRONMENT == Environment.DEVELOPMENT


def is_testing() -> bool:
    return CURRENT_ENVIRONMENT == Environment.TESTING


def is_production() -> bool:
    return CURRENT_ENVIRONMENT == Environment.PRODUCTION
"""
=========================================
CHITT - Voice Environment
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import platform
import socket
import importlib.util

import speech_recognition as sr
import pyttsx3


class VoiceEnvironment:

    def __init__(self):

        self.engine = pyttsx3.init()

    # ---------------------------------
    # Python Version
    # ---------------------------------

    def python_version(self):

        return platform.python_version()

    # ---------------------------------
    # Operating System
    # ---------------------------------

    def operating_system(self):

        return platform.system()

    # ---------------------------------
    # OS Version
    # ---------------------------------

    def os_version(self):

        return platform.version()

    # ---------------------------------
    # Machine
    # ---------------------------------

    def machine(self):

        return platform.machine()

    # ---------------------------------
    # Processor
    # ---------------------------------

    def processor(self):

        return platform.processor()

    # ---------------------------------
    # Internet Check
    # ---------------------------------

    def internet(self):

        try:

            socket.create_connection(

                ("8.8.8.8", 53),

                timeout=3

            )

            return True

        except Exception:

            return False

    # ---------------------------------
    # Microphone Check
    # ---------------------------------

    def microphone(self):

        try:

            sr.Microphone()

            return True

        except Exception:

            return False

    # ---------------------------------
    # Speaker Check
    # ---------------------------------

    def speaker(self):

        try:

            self.engine.say("")

            return True

        except Exception:

            return False

    # ---------------------------------
    # Library Check
    # ---------------------------------

    def library(self, name):

        return importlib.util.find_spec(name) is not None

    # ---------------------------------
    # Installed Libraries
    # ---------------------------------

    def libraries(self):

        return {

            "speech_recognition":
                self.library("speech_recognition"),

            "pyttsx3":
                self.library("pyttsx3"),

            "pyaudio":
                self.library("pyaudio")

        }

    # ---------------------------------
    # Environment Status
    # ---------------------------------

    def status(self):

        return {

            "python_version":
                self.python_version(),

            "operating_system":
                self.operating_system(),

            "os_version":
                self.os_version(),

            "machine":
                self.machine(),

            "processor":
                self.processor(),

            "internet":
                self.internet(),

            "microphone":
                self.microphone(),

            "speaker":
                self.speaker(),

            "libraries":
                self.libraries()

        }

    # ---------------------------------
    # Print Status
    # ---------------------------------

    def show(self):

        print("\n========== CHITT ==========\n")

        data = self.status()

        for key, value in data.items():

            print(f"{key} : {value}")

        print("\n===========================\n")


if __name__ == "__main__":

    env = VoiceEnvironment()

    env.show()
    