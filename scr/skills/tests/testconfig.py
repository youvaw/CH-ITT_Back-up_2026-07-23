from src.config.config_manager import ConfigManager # type: ignore

config = ConfigManager()

print("=" * 40)

print("App :", config.get("app_name"))

print("Version :", config.get("version"))

print("Wake Word :", config.get("wake_word"))

print("Voice :", config.get("voice"))

print("Language :", config.get("language"))

print("=" * 40)
