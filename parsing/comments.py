from bs4 import BeautifulSoup
from domain.comment import Comment
from domain.comment_status import CommentStatus

class CommentParser:
    @staticmethod
    def _parse_timestamp(comment) -> int | None:
        timestamp_el = comment.find(class_="commentthread_comment_timestamp")
        if timestamp_el and timestamp_el.get("data-timestamp"):
            return int(timestamp_el["data-timestamp"])
        fallback = comment.find(attrs={"data-timestamp": True})
        if fallback and fallback.get("data-timestamp"):
            return int(fallback["data-timestamp"])
        return None

    @staticmethod
    def _parse_author(comment) -> str | None:
        author_el = comment.find("a", class_="commentthread_author_link")
        if not author_el:
            return None
        return author_el.get_text(strip=True)

    @staticmethod
    def _parse_text(comment) -> str | None:
        text_el = comment.find(class_="commentthread_comment_text")
        if not text_el:
            return None
        return text_el.get_text(strip=True)

    @staticmethod
    def parse_comments(html: bytes) -> list[Comment]:
        soup = BeautifulSoup(html, "html.parser")
        comments = []

        for comment in soup.find_all("div", class_="commentthread_comment"):
            author = CommentParser._parse_author(comment)
            timestamp = CommentParser._parse_timestamp(comment)
            text = CommentParser._parse_text(comment)
            if author is None or timestamp is None or text is None:
                continue
            comments.append(Comment(author, timestamp, text))

        return comments

    @staticmethod
    def determine_comment_status(html: bytes, cookies_enabled: bool) -> CommentStatus:
        soup = BeautifulSoup(html, "html.parser")
        comment_entry = soup.find("div", class_="commentthread_entry_quotebox")

        if cookies_enabled == False:
            return CommentStatus.UNKNOWN
        elif comment_entry:
            return CommentStatus.ENABLED
        else:
            return CommentStatus.DISABLED
