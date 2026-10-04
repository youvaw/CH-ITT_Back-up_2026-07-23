"""
=========================================
CHITT - Notes Plugin
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import json
import os
from datetime import datetime

from plugins.plugin_base import PluginBase


class NotesPlugin(PluginBase):

    def __init__(self):

        super().__init__()

        self.name = "NotesPlugin"
        self.version = "1.0.0"
        self.description = "Notes Management Plugin"

        self.notes_file = "memory/notes.json"

        self.notes = []

        self.load()

    # ---------------------------------
    # Startup
    # ---------------------------------

    def start(self):

        print(f"{self.name} Started")

    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def stop(self):

        self.save()

        print(f"{self.name} Stopped")

    # ---------------------------------
    # Load Notes
    # ---------------------------------

    def load(self):

        if os.path.exists(self.notes_file):

            try:

                with open(

                    self.notes_file,

                    "r",

                    encoding="utf-8"

                ) as file:

                    self.notes = json.load(file)

            except Exception:

                self.notes = []

        else:

            self.notes = []

    # ---------------------------------
    # Save Notes
    # ---------------------------------

    def save(self):

        os.makedirs(

            os.path.dirname(self.notes_file),

            exist_ok=True

        )

        with open(

            self.notes_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.notes,

                file,

                indent=4,

                ensure_ascii=False

            )

    # ---------------------------------
    # Add Note
    # ---------------------------------

    def add(self, text):

        note = {

            "id": len(self.notes) + 1,

            "text": text,

            "created": datetime.now().isoformat()

        }

        self.notes.append(note)

        self.save()

        return note

    # ---------------------------------
    # Read Notes
    # ---------------------------------

    def read(self):

        return self.notes

    # ---------------------------------
    # Delete Note
    # ---------------------------------

    def delete(self, note_id):

        self.notes = [

            n for n in self.notes

            if n["id"] != note_id

        ]

        self.save()

        return True

    # ---------------------------------
    # Search Notes
    # ---------------------------------

    def search(self, keyword):

        keyword = keyword.lower()

        return [

            note

            for note in self.notes

            if keyword in note["text"].lower()

        ]

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, command, value=None):

        command = command.lower()

        if command == "add":

            return self.add(value)

        elif command == "read":

            return self.read()

        elif command == "delete":

            return self.delete(value)

        elif command == "search":

            return self.search(value)

        return {

            "success": False,

            "message": "Unknown command."

        }

    # ---------------------------------
    # Settings
    # ---------------------------------

    def settings(self):

        return {

            "notes_file": self.notes_file

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "plugin": self.name,

            "enabled": self.enabled,

            "notes": len(self.notes),

            "status": "OK"

        }


if __name__ == "__main__":

    plugin = NotesPlugin()

    plugin.start()

    plugin.add("This is my first CHITT note.")

    print(plugin.read())

    plugin.stop()
    
