import csv
import io

from output.serializers.base import OutputSerializer
from domain.scrape_result import ScrapeResult

class CSVSerializer(OutputSerializer):
    
    @staticmethod
    def serialize(data: ScrapeResult) -> str:
        if not data or not data.account_comments:
            return ""
        
        fieldnames = [
            "profile_name",
            "profile_url",
            "comments_status",
            "author_name",
            "text",
            "timestamp",
        ]
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for comment in data.account_comments:
            writer.writerow({
                "profile_name": data.profile_name,
                "profile_url": data.profile_url,
                "comments_status": data.comments_status,
                "author_name": comment.author_name,
                "text": comment.text,
                "timestamp": comment.timestamp,
            })
        
        return output.getvalue()