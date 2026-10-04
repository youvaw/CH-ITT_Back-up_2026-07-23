"""
=========================================
CHITT - Event Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class EventManager:

    def __init__(self):

        self.events = {}

    # ---------------------------------
    # Register Event
    # ---------------------------------

    def register(self, event_name, callback):

        if event_name not in self.events:

            self.events[event_name] = []

        self.events[event_name].append(callback)

    # ---------------------------------
    # Remove Event
    # ---------------------------------

    def unregister(self, event_name, callback):

        if event_name in self.events:

            if callback in self.events[event_name]:

                self.events[event_name].remove(callback)

    # ---------------------------------
    # Emit Event
    # ---------------------------------

    def emit(self, event_name, *args, **kwargs):

        if event_name not in self.events:

            return

        for callback in self.events[event_name]:

            try:

                callback(*args, **kwargs)

            except Exception as error:

                print(

                    f"Event Error [{event_name}] :",

                    error

                )

    # ---------------------------------
    # Get Events
    # ---------------------------------

    def get_events(self):

        return list(self.events.keys())

    # ---------------------------------
    # Clear Events
    # ---------------------------------

    def clear(self):

        self.events.clear()

    # ---------------------------------
    # Event Count
    # ---------------------------------

    def count(self):

        return len(self.events)

    # ---------------------------------
    # Status
    # ---------------------------------

    def status(self):

        print("\n===== EVENT MANAGER =====\n")

        print(

            "Registered Events :",

            self.count()

        )

        for event in self.get_events():

            print("•", event)

        print()


if __name__ == "__main__":

    manager = EventManager()

    def test_event(message):

        print("EVENT :", message)

    manager.register(

        "voice_command",

        test_event

    )

    manager.emit(

        "voice_command",

        "Hello CHITT"

    )

    manager.status()
    
