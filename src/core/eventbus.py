class EventBus:

    def __init__(self):
        self.events = {}

    def subscribe(self, event_name, callback):

        if event_name not in self.events:
            self.events[event_name] = []

        self.events[event_name].append(callback)

    def publish(self, event_name, data=None):

        if event_name not in self.events:
            return

        for callback in self.events[event_name]:
            callback(data)

    def unsubscribe(self, event_name, callback):

        if event_name in self.events:

            if callback in self.events[event_name]:
                self.events[event_name].remove(callback)
                
