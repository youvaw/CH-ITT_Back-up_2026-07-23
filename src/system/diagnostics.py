"""
CHITT Diagnostics Engine
Performs complete system diagnostics.
"""

from system.resource_monitor import ResourceMonitor


class Diagnostics:

    def __init__(self):

        self.monitor = ResourceMonitor()

    # ==================================================
    # CPU
    # ==================================================

    def cpu(self):

        return self.monitor.cpu_usage()

    # ==================================================
    # RAM
    # ==================================================

    def ram(self):

        return self.monitor.ram_usage()

    # ==================================================
    # Disk
    # ==================================================

    def disk(self):

        return self.monitor.disk_usage()

    # ==================================================
    # Battery
    # ==================================================

    def battery(self):

        return self.monitor.battery()

    # ==================================================
    # System
    # ==================================================

    def system(self):

        return self.monitor.system_info()

    # ==================================================
    # Complete Report
    # ==================================================

    def report(self):

        return {

            "CPU": self.cpu(),

            "RAM": self.ram(),

            "Disk": self.disk(),

            "Battery": self.battery(),

            "System": self.system()

        }

    # ==================================================
    # Print Report
    # ==================================================

    def print_report(self):

        report = self.report()

        print("=" * 60)

        print("CHITT Diagnostics Report")

        print("=" * 60)

        print()

        for key, value in report.items():

            print(f"{key} :")

            print(value)

            print()


if __name__ == "__main__":

    diagnostics = Diagnostics()

    diagnostics.print_report()
    
