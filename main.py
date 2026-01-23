import sys
import logging
import argparse

from services.comment_loader import CommentLoader
from domain.scrape_result import ScrapeResult
from config.env import EnvConfig
from cli.dry_run import DryRunManager
from cli.config_print_mode import ConfigPrintMode
from output.output_manager import OutputManager

from steam_client.exceptions import SteamRequestFailed, MaxPaginationDepthExceeded
import config.exceptions as config_exceptions
import cli.exceptions as cli_exceptions

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
    parser.add_argument("--no-dry-run", action="store_true", help="Explicitly disables dry-run mode, if its enabled in config")
    parser.add_argument(
        "--output-format", choices=["json", "csv", "xml", "text"], 
        required=False, help="Output format for scraped comments"
        )
    parser.add_argument(
        "--output-file", type=str, required=False, default=None, 
        help="Path to the output file where scraped comments will be saved"
        )
    
    return parser.parse_args()

def dry_run(self, message, *args, **kws):
    if self.isEnabledFor(DRY_RUN_LEVEL):
        self._log(DRY_RUN_LEVEL, message, args, **kws)

def config(self, message, *args, **kws):
    if self.isEnabledFor(CONFIG_LEVEL):
        self._log(CONFIG_LEVEL, message, args, **kws)

def setup_logger() -> logging.Logger:
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

    return logger

def extract_args(args, env_config: EnvConfig) -> None:
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
    if args.dry_run and args.no_dry_run:
        cli_exceptions.CLIArgumentConflict("Conflicting arguments: --dry-run and --no-dry-run cannot be used together.")
    if args.no_dry_run:
        env_config.dry_run = False
    if args.dry_run:
        env_config.dry_run = True
    if args.output_format:
        env_config.output_format = args.output_format
    if args.output_file:
        env_config.output_file = args.output_file

def main() -> int:
    logger = setup_logger()
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
        extract_args(args, env_config)

        if env_config.print_config_mode != ConfigPrintMode.NONE:
            if env_config.print_config_mode == ConfigPrintMode.FULL:
                logger.warning("Printing sensitive configuration values. Do NOT share this output.")

            logger.config("Resolved configuration:")

            for k, v in env_config.to_dict().items():
                logger.config("%s = %s", k, v)

            return 0
        else:
            logger.config("Configuration loaded successfully.")
            logger.info("Starting comment loading process.")

        if env_config.cookies_enabled == False:
            logger.warning("Proceeding without cookies may lead to incomplete data or request failures.")

        dry_run_manager: DryRunManager = DryRunManager(logger=logger, dry_run=env_config.dry_run)
        comment_loader: CommentLoader = CommentLoader(env_config, dry_run_manager)
        scrape_result: ScrapeResult = comment_loader.load_all()
        output_manager: OutputManager = OutputManager(
            format=env_config.output_format,
            file_path=env_config.output_file
        )

        if env_config.dry_run:
            logger.dry_run("Dry-run mode enabled: no requests were sent.")
            logger.dry_run("Exiting.")
            return 0
        
        logger.info(f"Comments loaded successfully for profile '{scrape_result.profile_name}' ({scrape_result.profile_url}).")
        logger.info(f"Total comments loaded: {len(scrape_result.account_comments)}")

        output_manager.output_data(scrape_result)

        logger.info("Output completed successfully.")

    except SteamRequestFailed as e:
        logger.error(f"Steam request failed: {e}")
        return 2
    except MaxPaginationDepthExceeded as e:
        logger.error(f"Pagination error: {e}")
        return 3
    except config_exceptions.ConfigError as e:
        logger.error(f"Configuration error: {e}")
        return 4
    except cli_exceptions.CLIArgumentConflict as e:
        logger.error(f"CLI argument error: {e}")
        return 5
    except Exception as e:
        logger.exception("Program unexpectedly crashed")
        return 1
    
    logger.info("Program ran successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())