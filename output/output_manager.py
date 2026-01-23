from domain.scrape_result import ScrapeResult
import output.serializers as serializers

class OutputManager:
    def __init__(self, format: str = "json", file_path: str | None = None):
        self.format = format
        self.file_path = file_path
    
    def output_data(self, data: ScrapeResult) -> None:
        match self.format:
            case "json":
                json_data = serializers.JSONSerializer.serialize(data)

                if self.file_path:
                    with open(self.file_path, "w", encoding="utf-8") as f:
                        f.write(json_data)
                else:
                    print(json_data)

            case "csv":
                csv_data = serializers.CSVSerializer.serialize(data)

                if self.file_path:
                    with open(self.file_path, "w", encoding="utf-8") as f:
                        f.write(csv_data)
                else:
                    print(csv_data)

            case "xml":
                xml_data = serializers.XMLSerializer.serialize(data)

                if self.file_path:
                    with open(self.file_path, "w", encoding="utf-8") as f:
                        f.write(xml_data)
                else:
                    print(xml_data)

            case "text":
                text_data = serializers.TextSerializer.serialize(data)

                if self.file_path:
                    with open(self.file_path, "w", encoding="utf-8") as f:
                        f.write(text_data)
                else:
                    print(text_data)

            case _:
                #TODO custom exception
                raise ValueError(f"Unsupported output format: {self.format}")