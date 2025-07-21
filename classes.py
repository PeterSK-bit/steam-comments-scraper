from datetime import datetime
from enum import Enum

class CommentStatus(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    UNKNOWN = "unknown"

class Comment:
    def __init__(self, author_name: str, timestamp:int, text: str):
        self._author_name = author_name
        self._timestamp = timestamp
        self._text = text
    
    def comment_tone(self) -> str:
        lowered = self._text.lower()
        if any(rep in lowered for rep in ("-rep", "- rep", "rep-")): return "Negative"
        if any(rep in lowered for rep in ("+rep", "+ rep", "rep+")): return "Positive"
        return "Neutral"

    def __str__(self) -> str:
        return f"At {datetime.fromtimestamp(self._timestamp)} user named {self._author_name} commented: {self._text}"
    
    #getters
    @property
    def author_name(self) -> str:
        return self._author_name
    
    @property
    def timestamp(self) -> int:
        return self._timestamp
    
    @property
    def text(self) -> str:
        return self._text

class User:
    def __init__(self, username:str, account_comments:list[Comment], comments_status: CommentStatus) -> None:
        self._username = username

        if all(isinstance(comment, Comment) for comment in account_comments):
            self._account_comments = account_comments
        else:
            self._account_comments = []

        self._comments_status = comments_status
    
    def append_comment(self, comment: Comment) -> bool:
        if not isinstance(comment, Comment): return False
        self._account_comments.append(comment)
        return True

    #getters
    @property
    def username(self) -> str:
        return self._username

    @property
    def account_comments(self) -> list[Comment]:
        return self._account_comments
    
    @property
    def comments_status(self) -> CommentStatus:
        return self._comments_status.value
    
    #string outputs
    def __str__(self) -> str:
        count = len(self._account_comments)
        comment_word = "comment" if count == 1 else "comments"
        
        if self._comments_status is not CommentStatus.UNKNOWN:
            return f"{self._username} has {count} {comment_word} on their profile and has comments {self._comments_status.value}."
        else:
            return f"{self._username} has {count} {comment_word} on their profile."
    
    def print_account_comments(self) -> None:
        for comment in self._account_comments:
            print(comment)