"""
CHITT AI
Configuration Loader
"""

"""
Resolve imports for both package layouts (top-level `config` or nested `src.config`).
This uses importlib to attempt importing the available module path so static
analyzers won't fail on the literal fallback import.
"""
import importlib

def _import_module_attr(module_paths, attr_name):
    for mod_path in module_paths:
        try:
            module = importlib.import_module(mod_path)
            return getattr(module, attr_name)
        except (ModuleNotFoundError, ImportError, AttributeError):
            continue
    raise ModuleNotFoundError(f"Could not import {attr_name} from any of: {module_paths}")

_settings_module_paths = ["config.settings", "src.config.settings"]
_environment_module_paths = ["config.environment", "src.config.environment"]

settings = _import_module_attr(_settings_module_paths, "settings")
CURRENT_ENVIRONMENT = _import_module_attr(_environment_module_paths, "CURRENT_ENVIRONMENT")
is_development = _import_module_attr(_environment_module_paths, "is_development")
is_testing = _import_module_attr(_environment_module_paths, "is_testing")
is_production = _import_module_attr(_environment_module_paths, "is_production")


class ConfigLoader:
    """Loads and provides application configuration."""

    def __init__(self):
        self.settings = settings
        self.environment = CURRENT_ENVIRONMENT

    def display(self):
        print("=" * 50)
        print("CHITT Configuration")
        print("=" * 50)
        print(f"App Name     : {self.settings.APP_NAME}")
        print(f"Version      : {self.settings.VERSION}")
        print(f"Author       : {self.settings.AUTHOR}")
        print(f"Environment  : {self.environment.value}")
        print(f"Debug Mode   : {self.settings.DEBUG}")
        print("=" * 50)


config = ConfigLoader()