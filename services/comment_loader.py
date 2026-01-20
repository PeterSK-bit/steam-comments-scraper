from domain.comment import Comment
from domain.user import User
from domain.comment_status import CommentStatus
from config.env import EnvConfig
from parsing.comments import CommentParser
from parsing.user import UserParser
from steam_client.steam_client import SteamClient
from cli.dry_run import DryRunManager

class CommentLoader:
    def __init__(self, env: EnvConfig, dry_run_manager: DryRunManager) -> None:
        self._env: EnvConfig = env
        self._steam_client: SteamClient = SteamClient(env, dry_run_manager)
        self._dry_run_manager: DryRunManager = dry_run_manager

    def load_all(self) -> User:
        extracted_comments: list[Comment] = []

        for page in range(1, self._env.max_pagination_depth + 1):
            page_content: bytes = self._dry_run_manager.execute(
                f"Fetch comments page {page}", self._steam_client.fetch_comments_page, page
                )
            if page_content is None: continue

            page_comments: list[Comment] = CommentParser.parse_comments(page_content)
            if not page_comments:
                break
            extracted_comments.extend(page_comments)
        
        if page_content is None:
            comment_status: CommentStatus = CommentStatus.UNKNOWN
            user_name: str = "DryRun User"
        else:
            comment_status:CommentStatus = CommentParser.determine_comment_status(page_content, self._env.cookies_enabled)
            page_content: bytes = self._steam_client.fetch_comments_page(1)
            user_name: str = UserParser.parse_user(page_content)

        return User(user_name, extracted_comments, comment_status)