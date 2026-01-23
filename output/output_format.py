from enum import Enum

from config.exceptions import ConfigError

class OutputFormat(Enum):
    JSON = "json"
    CSV = "csv"
    XML = "xml"
    TEXT = "text"

    @classmethod
    def parse(cls, raw: str) -> "OutputFormat":
        try:
            return cls(raw)
        except ValueError:
            raise ConfigError("output_format must be one of: json, csv, xml, text")