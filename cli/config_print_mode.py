from enum import Enum

from config.exceptions import ConfigError

class ConfigPrintMode(str, Enum):
    SAFE = "safe"
    FULL = "full"
    NONE = "none"

    @classmethod
    def parse(cls, raw: str) -> "ConfigPrintMode":
        try:
            return cls(raw)
        except ValueError:
            raise ConfigError("print_config_mode must be one of: safe, full, none")
