import sys
import logging
import argparse
from services.comment_loader import CommentLoader
from domain.user import User
from config.env import EnvConfig
from cli.dry_run import DryRunManager
from cli.config_print_mode import ConfigPrintMode

from steam_client.exceptions import SteamRequestFailed
from steam_client.exceptions import MaxPaginationDepthExceeded
import config.exceptions as config_exceptions

DRY_RUN_LEVEL = 25
CONFIG_LEVEL = 15

def parse_args():
    parser = argparse.ArgumentParser(description="Steam comment loader")
    parser.add_argument("--steam-login-secure", type=str, required=False, help="Steam login secure cookie value")
    parser.add_argument("--session-id", type=str, required=False, help="Steam session ID cookie value")
    parser.add_argument("--max-pages", type=int, required=False, help="Maximum number of comment pages to load")
    parser.add_argument("--user-url", type=str, required=False, help="Full URL to the user's Steam profile")
    parser.add_argument("--request-delay-ms", type=int, required=False, help="Delay between requests in milliseconds")
    parser.add_argument("--env-file", type=str, required=False, help="Path to the environment file")
    parser.add_argument("--print-config-mode", choices=[m.value for m in ConfigPrintMode], required=False,
        help="Print resolved configuration and exit. Modes: safe (masked secrets), full (includes sensitive data), none."
    )
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without sending HTTP requests")
    return parser.parse_args()

def dry_run(self, message, *args, **kws):
    if self.isEnabledFor(DRY_RUN_LEVEL):
        self._log(DRY_RUN_LEVEL, message, args, **kws)

def config(self, message, *args, **kws):
    if self.isEnabledFor(CONFIG_LEVEL):
        self._log(CONFIG_LEVEL, message, args, **kws)

def main() -> int:
    logging.basicConfig(
        level=CONFIG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger: logging.Logger = logging.getLogger(__name__)

    logging.addLevelName(DRY_RUN_LEVEL, "DRY-RUN")
    logging.Logger.dry_run = dry_run

    logging.addLevelName(CONFIG_LEVEL, "CONFIG")
    logging.Logger.config = config
    
    args = parse_args()

    try:
        env_config = EnvConfig(path=args.env_file) if args.env_file else EnvConfig()
        env_config.apply_env()
    except (config_exceptions.EnvFileNotFound, config_exceptions.EnvLoadError) as e:
        logger.warning(f"Environment loading error: {e} - if you are using CLI args, ignore this.")
    except config_exceptions.EnvFilePathNotProvided as e:
        logger.warning(f"{e} - if you are using CLI args, ignore this.")
    except config_exceptions.ConfigError as e:
        logger.error(f"Configuration error: {e}")
        return 4

    try:
        if args.steam_login_secure:
            env_config.steam_login_secure = args.steam_login_secure
        if args.session_id:
            env_config.session_id = args.session_id
        if args.max_pages:
            env_config.max_pagination_depth = args.max_pages
        if args.user_url:
            env_config.steam_url = args.user_url
        if args.request_delay_ms:
            env_config.request_delay_ms = args.request_delay_ms
        if args.print_config_mode:
            env_config.print_config_mode = ConfigPrintMode.parse(args.print_config_mode)
        if args.dry_run:
            env_config.dry_run = True

        if env_config.print_config_mode != ConfigPrintMode.NONE:
            if env_config.print_config_mode == ConfigPrintMode.FULL:
                logger.warning("Printing sensitive configuration values. Do NOT share this output.")

            logger.config("Resolved configuration:")

            for k, v in env_config.to_dict().items():
                logger.config("%s = %s", k, v)

            return 0

        if env_config.cookies_enabled == False:
            logger.warning("Proceeding without cookies may lead to incomplete data or request failures.")

        dry_run_manager: DryRunManager = DryRunManager(logger=logger, dry_run=env_config.dry_run)
        comment_loader: CommentLoader = CommentLoader(env_config, dry_run_manager)
        user: User = comment_loader.load_all()

        if env_config.dry_run:
            logger.dry_run("Dry-run mode enabled: no requests were sent.")
            logger.dry_run("Exiting.")
            return 0
        
        logger.info(user)
        for c in user.account_comments:
            logger.info(c)

    except SteamRequestFailed as e:
        logger.error(f"Steam request failed: {e}")
        return 2
    except MaxPaginationDepthExceeded as e:
        logger.error(f"Pagination error: {e}")
        return 3
    except config_exceptions.ConfigError as e:
        logger.error(f"Configuration error: {e}")
        return 4
    except Exception as e:
        logger.exception("Program unexpectedly crashed")
        return 1
    
    logger.info("Program ran successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())