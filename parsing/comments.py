from bs4 import BeautifulSoup
from domain.comment import Comment
from domain.comment_status import CommentStatus

class CommentParser:
    @staticmethod
    def parse_comments(html: bytes) -> list[Comment]:
        soup = BeautifulSoup(html, "html.parser")
        comments = []

        for comment in soup.find_all("div", class_="commentthread_comment"):
            author = comment.find("a", class_="commentthread_author_link").text.strip()
            timestamp = int(comment.find("span", class_="commentthread_comment_timestamp")["data-timestamp"])
            text = comment.find("div", class_="commentthread_comment_text").text.strip()
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