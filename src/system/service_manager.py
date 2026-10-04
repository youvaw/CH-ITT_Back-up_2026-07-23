"""
CHITT Service Manager
Manages all core system services.
"""

from logger.logger import Logger


class ServiceManager:

    def __init__(self):

        self.logger = Logger()

        self.services = {}

    # ==================================================
    # Register Service
    # ==================================================

    def register(self, name, service):

        self.services[name] = service

        self.logger.info(f"Service Registered : {name}")

    # ==================================================
    # Get Service
    # ==================================================

    def get(self, name):

        return self.services.get(name)

    # ==================================================
    # Start All Services
    # ==================================================

    def start_all(self):

        self.logger.info("Starting Services...")

        for name, service in self.services.items():

            try:

                if hasattr(service, "start"):

                    service.start()

                self.logger.info(f"{name} Started")

            except Exception as error:

                self.logger.error(f"{name} : {error}")

    # ==================================================
    # Stop All Services
    # ==================================================

    def stop_all(self):

        self.logger.info("Stopping Services...")

        for name, service in self.services.items():

            try:

                if hasattr(service, "stop"):

                    service.stop()

                self.logger.info(f"{name} Stopped")

            except Exception as error:

                self.logger.error(f"{name} : {error}")

    # ==================================================
    # Restart Service
    # ==================================================

    def restart(self, name):

        service = self.services.get(name)

        if service is None:

            return False

        try:

            if hasattr(service, "stop"):

                service.stop()

            if hasattr(service, "start"):

                service.start()

            self.logger.info(f"{name} Restarted")

            return True

        except Exception as error:

            self.logger.error(error)

            return False

    # ==================================================
    # Service Status
    # ==================================================

    def status(self):

        result = {}

        for name, service in self.services.items():

            if hasattr(service, "running"):

                result[name] = service.running

            else:

                result[name] = "Unknown"

        return result

    # ==================================================
    # Registered Services
    # ==================================================

    def list_services(self):

        return list(self.services.keys())


if __name__ == "__main__":

    manager = ServiceManager()

    print(manager.list_services())
    
