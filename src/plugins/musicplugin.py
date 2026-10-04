"""
=========================================
CHITT - Music Plugin
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import subprocess
import platform

from plugins.plugin_base import PluginBase


class MusicPlugin(PluginBase):

    def __init__(self):

        super().__init__()

        self.name = "MusicPlugin"
        self.version = "1.0.0"
        self.description = "Music Control Plugin"

        self.current_song = None
        self.volume = 50
        self.is_playing = False

    # ---------------------------------
    # Startup
    # ---------------------------------

    def start(self):

        print(f"{self.name} Started")

    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def stop(self):

        print(f"{self.name} Stopped")

    # ---------------------------------
    # Play File
    # ---------------------------------

    def play(self, filepath):

        if not os.path.exists(filepath):

            return {
                "success": False,
                "message": "File not found."
            }

        try:

            system = platform.system()

            if system == "Windows":
                os.startfile(filepath)

            elif system == "Darwin":
                subprocess.Popen(["open", filepath])

            else:
                subprocess.Popen(["xdg-open", filepath])

            self.current_song = filepath
            self.is_playing = True

            return {
                "success": True,
                "song": filepath
            }

        except Exception as error:

            return {
                "success": False,
                "message": str(error)
            }

    # ---------------------------------
    # Pause
    # ---------------------------------

    def pause(self):

        return {
            "success": True,
            "message": "Pause command sent."
        }

    # ---------------------------------
    # Resume
    # ---------------------------------

    def resume(self):

        return {
            "success": True,
            "message": "Resume command sent."
        }

    # ---------------------------------
    # Stop Music
    # ---------------------------------

    def stop_music(self):

        self.is_playing = False

        return {
            "success": True,
            "message": "Stop command sent."
        }

    # ---------------------------------
    # Volume
    # ---------------------------------

    def set_volume(self, value):

        value = max(0, min(100, int(value)))

        self.volume = value

        return {
            "success": True,
            "volume": self.volume
        }

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, command, value=None):

        command = command.lower()

        if command == "play":

            return self.play(value)

        elif command == "pause":

            return self.pause()

        elif command == "resume":

            return self.resume()

        elif command == "stop":

            return self.stop_music()

        elif command == "volume":

            return self.set_volume(value)

        return {
            "success": False,
            "message": "Unknown command."
        }

    # ---------------------------------
    # Settings
    # ---------------------------------

    def settings(self):

        return {
            "default_volume": self.volume
        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {
            "plugin": self.name,
            "enabled": self.enabled,
            "playing": self.is_playing,
            "volume": self.volume,
            "status": "OK"
        }


if __name__ == "__main__":

    plugin = MusicPlugin()

    plugin.start()

    print(plugin.health())

    plugin.stop()
    
