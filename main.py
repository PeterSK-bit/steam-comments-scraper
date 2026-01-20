import sys
import logging
import argparse
from services.comment_loader import CommentLoader
from domain.user import User
from config.env import EnvConfig

from steam_client.exceptions import SteamRequestFailed
from steam_client.exceptions import MaxPaginationDepthExceeded
from config.exceptions import EnvFileNotFound, EnvLoadError, ConfigError

def parse_args():
    parser = argparse.ArgumentParser(description="Steam comment loader")
    parser.add_argument("--steam-login-secure", type=str, required=False, help="Steam login secure cookie value")
    parser.add_argument("--session-id", type=str, required=False, help="Steam session ID cookie value")
    parser.add_argument("--max-pages", type=int, required=False, help="Maximum number of comment pages to load")
    parser.add_argument("--user-url", type=str, required=False, help="Full URL to the user's Steam profile")
    parser.add_argument("--request-delay-ms", type=int, required=False, help="Delay between requests in milliseconds")
    return parser.parse_args()

def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    
    args = parse_args()

    try:
        env_config = EnvConfig()
        env_config._load_env()
    except (EnvFileNotFound, EnvLoadError) as e:
        logger.warning(f"Environment loading error: {e} - if you are using CLI args, ignore this.")

    try:
        if args.steam_login_secure:
            env_config.steam_login_secure = args.steam_login_secure
        if args.session_id:
            env_config.session_id = args.session_id
        if args.max_pages:
            env_config.max_pagination_depth = args.max_pages
        if args.user_url:
            env_config.steam_url = args.user_url
        if args.request_delay:
            env_config.request_delay_ms = args.request_delay

        env_config._normalize_vars()

        if env_config.cookies_enabled == False:
            logger.warning("Proceeding without cookies may lead to incomplete data or request failures.")

        comment_loader = CommentLoader(env_config)
        user: User = comment_loader.load_all()
        
        logger.info(user)
        for c in user.account_comments:
            logger.info(c)

    except SteamRequestFailed as e:
        logger.error(f"Steam request failed: {e}")
        return 2
    except MaxPaginationDepthExceeded as e:
        logger.error(f"Pagination error: {e}")
        return 3
    except ConfigError as e:
        logger.error(f"Configuration error: {e} - set up env file correctly or use CLI args.")
        return 4
    except Exception as e:
        logger.exception("Program unexpectedly crashed")
        return 1
    
    logger.info("Program ran successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())