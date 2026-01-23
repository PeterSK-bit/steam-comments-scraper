from domain.scrape_result import ScrapeResult
from output.output_format import OutputFormat
import output.serializers as serializers

class OutputManager:
    _serializers = {
        OutputFormat.JSON: serializers.JSONSerializer,
        OutputFormat.CSV: serializers.CSVSerializer,
        OutputFormat.XML: serializers.XMLSerializer,
        OutputFormat.TEXT: serializers.TextSerializer,
    }

    def __init__(self, format: OutputFormat = OutputFormat.JSON, file_path: str | None = None):
        self.format = format
        self.file_path = file_path

    def output_data(self, data: ScrapeResult) -> None:
        serializer = self._serializers[self.format]

        try:
            serialized = serializer.serialize(data)
        except Exception as e:
            raise RuntimeError(f"Serialization failed for format '{self.format}'") from e

        if self.file_path:
            self._write_to_file(serialized)
        else:
            print(serialized)

    def _write_to_file(self, content: str) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise IOError(f"Failed to write output to '{self.file_path}'") from e
