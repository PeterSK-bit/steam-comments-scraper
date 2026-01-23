from dataclasses import asdict
from enum import Enum
import json

from output.serializers.base import OutputSerializer
from domain.scrape_result import ScrapeResult

class JSONSerializer(OutputSerializer):
    
    @staticmethod
    def serialize(data: ScrapeResult) -> str:
        return json.dumps(asdict(data), default=lambda o: o.value if isinstance(o, Enum) else str(o), indent=4, ensure_ascii=False)