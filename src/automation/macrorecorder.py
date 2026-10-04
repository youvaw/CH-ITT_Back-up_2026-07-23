"""
=========================================
CHITT - Macro Recorder
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


class MacroRecorder:

    def __init__(self):

        self.recording = False

        self.events = []

        self.start_time = None

    # ---------------------------------
    # Start Recording
    # ---------------------------------

    def start(self):

        self.events = []

        self.recording = True

        self.start_time = time.time()

        keyboard.hook(self._keyboard_event)

        mouse.hook(self._mouse_event)

        return {

            "success": True,

            "message": "Recording Started"

        }

    # ---------------------------------
    # Stop Recording
    # ---------------------------------

    def stop(self):

        self.recording = False

        keyboard.unhook_all()

        mouse.unhook_all()

        return {

            "success": True,

            "events": len(self.events)

        }

    # ---------------------------------
    # Keyboard Event
    # ---------------------------------

    def _keyboard_event(self, event):

        if not self.recording:

            return

        self.events.append({

            "type": "keyboard",

            "name": event.name,

            "event": event.event_type,

            "time": time.time() - self.start_time

        })

    # ---------------------------------
    # Mouse Event
    # ---------------------------------

    def _mouse_event(self, event):

        if not self.recording:

            return

        self.events.append({

            "type": "mouse",

            "data": str(event),

            "time": time.time() - self.start_time

        })

    # ---------------------------------
    # Save Macro
    # ---------------------------------

    def save(self, filename):

        with open(

            filename,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.events,

                file,

                indent=4

            )

        return {

            "success": True,

            "file": filename

        }

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

        return self.events

    # ---------------------------------
    # Clear
    # ---------------------------------

    def clear(self):

        self.events = []

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return {

            "recording": self.recording,

            "events": len(self.events)

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "MacroRecorder",

            "status": "OK",

            "recording": self.recording

        }


if __name__ == "__main__":

    recorder = MacroRecorder()

    print(recorder.health())
    
