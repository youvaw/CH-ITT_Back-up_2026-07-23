class ServiceContainer:

    def __init__(self):

        self.services = {}

    def register(self, name, service):

        self.services[name] = service

    def get(self, name):

        return self.services.get(name)

    def exists(self, name):

        return name in self.services

    def remove(self, name):

        if name in self.services:
            del self.services[name]

    def all_services(self):

        return list(self.services.keys())
    
