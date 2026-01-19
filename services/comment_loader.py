from domain.comment import Comment
from domain.user import User
from domain.comment_status import CommentStatus
from config.env import EnvConfig
from parsing.comments import CommentParser
from parsing.user import UserParser
from steam_client.steam_client import SteamClient

class CommentLoader:
    def __init__(self, env: EnvConfig) -> None:
        self._env: EnvConfig = env
        self._steam_client: SteamClient = SteamClient(env)

    def load_all(self) -> User:
        page: int = 1
        extracted_comments: list[Comment] = []

        while page <= self._env.max_pagination_depth:
            page_content: bytes = self._steam_client.fetch_comments_page(page)
            page_comments: list[Comment] = CommentParser.parse_comments(page_content)
            if not page_comments:
                break
            extracted_comments.extend(page_comments)
            page += 1
        
        comment_status:CommentStatus = CommentParser.determine_comment_status(page_content, self._env.cookies_enabled)
        page_content: bytes = self._steam_client.fetch_comments_page(1)
        user_name: str = UserParser.parse_user(page_content)

        return User(user_name, extracted_comments, comment_status)