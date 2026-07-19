"""
CHITT AI
System Information
"""

import platform
import socket
import psutil


class SystemInfo:

    def get_os(self):

        return platform.system()

    def get_os_version(self):

        return platform.version()

    def get_processor(self):

        return platform.processor()

    def get_hostname(self):

        return socket.gethostname()

    def get_ip(self):

        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "Unavailable"

    def get_ram(self):

        ram = psutil.virtual_memory()

        return f"{round(ram.total / (1024**3), 2)} GB"

    def get_ram_usage(self):

        ram = psutil.virtual_memory()

        return f"{ram.percent}%"

    def get_cpu_usage(self):

        return f"{psutil.cpu_percent(interval=1)}%"

    def get_disk_usage(self):

        disk = psutil.disk_usage("/")

        return f"{disk.percent}%"
    