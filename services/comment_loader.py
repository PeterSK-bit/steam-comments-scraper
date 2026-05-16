from domain.comment import Comment
from domain.scrape_result import ScrapeResult
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

    def load_all(self) -> ScrapeResult:
        extracted_comments: list[Comment] = []
        first_page_content: bytes | None = None
        user_url: str = self._env.steam_url.rstrip("/").removesuffix("/allcomments")

        for page in range(1, self._env.max_pagination_depth + 1):
            page_content: bytes = self._dry_run_manager.execute(
                f"Fetch comments page {page}", self._steam_client.fetch_comments_page, page
                )
            if page_content is None:
                continue
            if first_page_content is None:
                first_page_content = page_content

            page_comments: list[Comment] = CommentParser.parse_comments(page_content)
            if not page_comments:
                break
            extracted_comments.extend(page_comments)
        
        if first_page_content is None:
            comment_status: CommentStatus = CommentStatus.UNKNOWN
            user_name: str = "DryRun User"
        else:
            comment_status: CommentStatus = CommentParser.determine_comment_status(
                first_page_content, self._env.cookies_enabled
            )
            user_name: str = UserParser.parse_user(first_page_content) or "Unknown"

        return ScrapeResult(user_name, user_url, extracted_comments, comment_status)