"""
=========================================
CHITT - Macro Player
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import time
import keyboard
import mouse


class MacroPlayer:

    def __init__(self):

        self.events = []

        self.playing = False

    # ---------------------------------
    # Load Macro
    # ---------------------------------

    def load(self, filename):

        with open(

            filename,

            "r",

            encoding="utf-8"

        ) as file:

            self.events = json.load(file)

        return {

            "success": True,

            "events": len(self.events)

        }

    # ---------------------------------
    # Play Macro
    # ---------------------------------

    def play(self):

        if not self.events:

            return {

                "success": False,

                "message": "No macro loaded."

            }

        self.playing = True

        previous_time = 0

        for event in self.events:

            delay = event["time"] - previous_time

            if delay > 0:

                time.sleep(delay)

            previous_time = event["time"]

            if event["type"] == "keyboard":

                if event["event"] == "down":

                    keyboard.press(

                        event["name"]

                    )

                elif event["event"] == "up":

                    keyboard.release(

                        event["name"]

                    )

            elif event["type"] == "mouse":

                # Placeholder
                # Mouse replay parser can
                # be extended later.
                pass

        self.playing = False

        return {

            "success": True,

            "played": len(self.events)

        }

    # ---------------------------------
    # Stop Playback
    # ---------------------------------

    def stop(self):

        self.playing = False

        keyboard.release_all()

        return {

            "success": True

        }

    # ---------------------------------
    # Clear
    # ---------------------------------

    def clear(self):

        self.events = []

    # ---------------------------------
    # Status
    # ---------------------------------

    def status(self):

        return {

            "playing": self.playing,

            "events": len(self.events)

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "MacroPlayer",

            "status": "OK",

            "playing": self.playing

        }


if __name__ == "__main__":

    player = MacroPlayer()

    print(player.health())
    
