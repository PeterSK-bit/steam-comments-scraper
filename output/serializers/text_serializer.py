from datetime import datetime

from output.serializers.base import OutputSerializer
from domain.scrape_result import ScrapeResult

class TextSerializer(OutputSerializer):

    @staticmethod
    def serialize(data: ScrapeResult) -> str:
        """
        Convert ScrapeResult into a plain text representation.
        """

        lines = [
            f"Profile Name: {data.profile_name}",
            f"Profile URL: {data.profile_url}",
            f"Total Comments: {len(data.account_comments)}",
            "Comments:",
        ]

        for comment in data.account_comments:
            lines.append(
                f"At {datetime.fromtimestamp(comment.timestamp)} user named {comment.author_name} commented: {comment.text}"
                )
        
        return "\n".join(lines)