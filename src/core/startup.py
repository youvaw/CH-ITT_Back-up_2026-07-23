# Service Container Import
try:
    from core.container import ServiceContainer
except ModuleNotFoundError:
    from src.core.container import ServiceContainer

# Settings Manager Import
try:
    from settings.settingsmanager import SettingsManager
except ModuleNotFoundError:
    from src.settings.settingsmanager import SettingsManager

# Memory Manager Import
try:
    from memory.memorymanager import MemoryManager
except ModuleNotFoundError:
    from src.memory.memorymanager import MemoryManager


def start():
    """CHITT AI System Startup Process"""
    print("=" * 40)
    print("CHITT AI Starting...")
    print("=" * 40)

    # 1. Service Container Initialize
    container = ServiceContainer()
    print("Service Container: OK")

    # 2. Settings Manager Register
    settings = SettingsManager()
    container.register("settings", settings)
    print("Settings Manager: OK")

    # 3. Memory Manager Register
    try:
        memory = MemoryManager()
        container.register("memory", memory)
        print("Memory Manager: OK")
    except Exception as e:
        print(f"Memory Manager Warning: {e}")

    print("Core system: OK")
    print("=" * 40)

    return container


if __name__ == "__main__":
    start()

