from requests import get, exceptions

from config.env import EnvConfig
from steam_client.rate_limiter import RateLimiter
from cli.dry_run import DryRunManager

from steam_client.exceptions import SteamRequestFailed, MaxPaginationDepthExceeded

class SteamClient:
    def __init__(self, env: EnvConfig, dry_run_manager: DryRunManager) -> None:
        self._env = env
        self._rate_limiter = RateLimiter(self._env.request_delay_ms)
        if not self._env.steam_url.endswith("/allcomments"): self._env.steam_url += "/allcomments"
        self._dry_run_manager: DryRunManager = dry_run_manager
    
    def fetch_comments_page(self, page: int) -> bytes:
        return self._dry_run_manager.execute(f"Fetch comments page {page}", self._fetch_comments_page, page)

    def _fetch_comments_page(self, page: int) -> bytes:
        if page > self._env.max_pagination_depth:
            raise MaxPaginationDepthExceeded(f"Max pagination depth of {self._env.max_pagination_depth} exceeded")

        self._rate_limiter.wait()
        
        try:
            response = get(
                f"{self._env.steam_url}?ctp={page}",
                cookies=self._env.cookies
            )
            response.raise_for_status()
        except exceptions.HTTPError as e:
            raise SteamRequestFailed(f"HTTP {e.response.status_code}") from e
        except exceptions.RequestException as e:
            raise SteamRequestFailed("Network error") from e
        except Exception as e:
            raise SteamRequestFailed("Unknown error") from e
        
        return response.content