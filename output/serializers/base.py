from abc import ABC, abstractmethod
from domain.scrape_result import ScrapeResult

class OutputSerializer(ABC):

    @abstractmethod
    def serialize(self, result: ScrapeResult) -> str:
        """
        Convert ScrapeResult into a string representation.
        """
        pass
