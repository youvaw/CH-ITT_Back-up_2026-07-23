from src.system.system_info import SystemInfo # type: ignore

system = SystemInfo()

print("=" * 50)

print("OS :", system.get_os())

print("Version :", system.get_os_version())

print("Processor :", system.get_processor())

print("Host :", system.get_hostname())

print("IP :", system.get_ip())

print("RAM :", system.get_ram())

print("RAM Usage :", system.get_ram_usage())

print("CPU :", system.get_cpu_usage())

print("Disk :", system.get_disk_usage())

print("=" * 50)
