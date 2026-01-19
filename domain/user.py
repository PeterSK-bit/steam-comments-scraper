from domain.comment import Comment
from domain.comment_status import CommentStatus

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