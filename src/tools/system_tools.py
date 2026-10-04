# -*- coding: utf-8 -*-

import os
import platform
import socket
import shutil

import psutil


class SystemTools:
    """
    Local system information and monitoring tools for MYX.

    This module does not depend on:
    - Gemini
    - OpenAI
    - Internet
    - Voice
    """

    @staticmethod
    def system_info():
        memory = psutil.virtual_memory()
        disk = shutil.disk_usage(os.path.abspath(os.sep))

        return {
            "computer": socket.gethostname(),
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "cpu_percent": psutil.cpu_percent(interval=0.2),
            "ram_total_gb": round(memory.total / (1024 ** 3), 2),
            "ram_used_gb": round(memory.used / (1024 ** 3), 2),
            "ram_percent": memory.percent,
            "disk_total_gb": round(disk.total / (1024 ** 3), 2),
            "disk_used_gb": round(disk.used / (1024 ** 3), 2),
            "disk_percent": round(
                (disk.used / disk.total) * 100, 2
            ),
        }

    @staticmethod
    def cpu():
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "cpu_count": psutil.cpu_count(),
            "logical_cpu_count": psutil.cpu_count(logical=True),
        }

    @staticmethod
    def memory():
        memory = psutil.virtual_memory()

        return {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "used_gb": round(memory.used / (1024 ** 3), 2),
            "available_gb": round(memory.available / (1024 ** 3), 2),
            "percent": memory.percent,
        }

    @staticmethod
    def battery():
        battery = psutil.sensors_battery()

        if battery is None:
            return {
                "available": False,
                "message": "Battery information is not available.",
            }

        return {
            "available": True,
            "percent": battery.percent,
            "charging": battery.power_plugged,
        }

    @staticmethod
    def disk():
        disk = shutil.disk_usage(os.path.abspath(os.sep))

        return {
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
            "percent": round((disk.used / disk.total) * 100, 2),
        }

    @staticmethod
    def health():
        return {
            "module": "SystemTools",
            "status": "OK",
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "python": platform.python_version(),
        }


if __name__ == "__main__":
    print("=" * 60)
    print("MYX SYSTEM TOOLS TEST")
    print("=" * 60)

    print("\nHEALTH:")
    print(SystemTools.health())

    print("\nCPU:")
    print(SystemTools.cpu())

    print("\nMEMORY:")
    print(SystemTools.memory())

    print("\nBATTERY:")
    print(SystemTools.battery())

    print("\nDISK:")
    print(SystemTools.disk())

    print("\nSYSTEM INFO:")
    print(SystemTools.system_info())

    print("\nSYSTEM TOOLS : PASS")
    print("=" * 60)