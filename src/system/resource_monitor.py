"""
CHITT Resource Monitor
Monitors CPU, RAM, Disk, Battery and System Performance.
"""

import platform
import psutil


class ResourceMonitor:

    def __init__(self):

        self.system = platform.system()

    # ==================================================
    # CPU
    # ==================================================

    def cpu_usage(self):

        return psutil.cpu_percent(interval=1)

    # ==================================================
    # RAM
    # ==================================================

    def ram_usage(self):

        memory = psutil.virtual_memory()

        return {

            "total": round(memory.total / (1024 ** 3), 2),

            "used": round(memory.used / (1024 ** 3), 2),

            "available": round(memory.available / (1024 ** 3), 2),

            "percent": memory.percent

        }

    # ==================================================
    # Disk
    # ==================================================

    def disk_usage(self):

        disk = psutil.disk_usage("/")

        return {

            "total": round(disk.total / (1024 ** 3), 2),

            "used": round(disk.used / (1024 ** 3), 2),

            "free": round(disk.free / (1024 ** 3), 2),

            "percent": disk.percent

        }

    # ==================================================
    # Battery
    # ==================================================

    def battery(self):

        battery = psutil.sensors_battery()

        if battery is None:

            return None

        return {

            "percent": battery.percent,

            "charging": battery.power_plugged

        }

    # ==================================================
    # Boot Time
    # ==================================================

    def boot_time(self):

        return psutil.boot_time()

    # ==================================================
    # System Info
    # ==================================================

    def system_info(self):

        return {

            "OS": platform.system(),

            "Release": platform.release(),

            "Version": platform.version(),

            "Machine": platform.machine(),

            "Processor": platform.processor()

        }

    # ==================================================
    # Complete Report
    # ==================================================

    def report(self):

        return {

            "cpu": self.cpu_usage(),

            "ram": self.ram_usage(),

            "disk": self.disk_usage(),

            "battery": self.battery(),

            "system": self.system_info()

        }


if __name__ == "__main__":

    monitor = ResourceMonitor()

    print("=" * 50)

    print("CHITT Resource Monitor")

    print("=" * 50)

    print()

    print("CPU")

    print(monitor.cpu_usage(), "%")

    print()

    print("RAM")

    print(monitor.ram_usage())

    print()

    print("Disk")

    print(monitor.disk_usage())

    print()

    print("Battery")

    print(monitor.battery())

    print()

    print("System")

    print(monitor.system_info())
    
