from dataclasses import dataclass

from domain.comment import Comment
from domain.comment_status import CommentStatus

@dataclass(frozen=True)
class ScrapeResult:
    profile_name: str
    profile_url: str
    account_comments: list[Comment]
    comments_status: CommentStatus