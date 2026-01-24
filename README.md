# Steam Comments Scraper

A Python CLI application for scraping public comments from a Steam Community profile.  
Supports pagination, comment visibility detection, structured domain models, logging, and multiple configuration sources (ENV + CLI).

---

## Features

- Scrapes all public profile comments (with pagination)
- Detects comment visibility status (enabled / disabled / unknown)
- Works with or without authentication cookies
- CLI-first design with ENV fallback
- Structured OOP architecture (config / domain / services)
- Centralized logging
- Safe error propagation with explicit failure modes

---

## Installation
### 1. Clone repository
```
git clone https://github.com/PeterSK-bit/steam-comments-scraper.git
cd steam-comments-scraper
```
### 2. Install all dependencies
```
pip install -r requirements.txt
```

---

## Environment Configuration
Create a **.env** file in the `/config` of the project with the following structure:
```
steam_url=https://steamcommunity.com/id/yourSteamID
steamLoginSecure=YOUR_STEAM_LOGINSECURE_COOKIE
sessionid=YOUR_SESSIONID_COOKIE
MAX_PAGINATION_DEPTH=10
request_delay_ms=0
print_config_mode=none
dry_run=False
output_format=json
output_file=data.json
```

> To get the cookies, log in to Steam in your browser, open **Developer Tools (F12) > Application > Cookies**, and copy the values for __steamLoginSecure__ and __sessionid__.

**Notes:**
- Cookies are optional.
- Without cookies, the scraper runs in restricted mode.
- Missing `.env` file does not stop execution (a warning is logged).
- Default `MAX_PAGINATION_DEPTH` is set at **100**.
- Default `request_delay_ms` is set to **0**.
- `print_config_mode` is a diagnostic option used to print the resolved configuration and exit.
  - `print_config_mode` modes: full, safe, none.
  - Default value of `print_config_mode` is **none** (standard for normal usage).
- `dry_run` is a diagnostic option used to check algorithm correctness without fetching any data.
  - Default value of `dry_run` is **False** (standard for normal usage).
- `output_format` choices: json, xml, csv and text
- `output_file` default: None
  - If not spetified, output would be printed to console

---

## Run script
```
python main.py
```

### CLI arguments
```
python main.py \
  --user-url https://steamcommunity.com/id/yourSteamID \
  --max-pages 50 \
  --steam-login-secure <cookie> \
  --session-id <cookie> \
  --request-delay-ms 500 \
  --env-file config/.env \
  --print-config-mode safe \
  --dry-run \
  --no-dry-run \
  --output-format json \
  --output-file data.json
```

### CLI arguments explaination
- `--user-url` 
  - Steam Community profile URL to scrape.
  - Required if not provided via .env.
- `--max-pages`
  - Maximum number of comment pages to fetch.
  - Overrides MAX_PAGINATION_DEPTH from .env.
  - Default: 100.
- `--steam-login-secure` 
  - Value of the steamLoginSecure cookie.
  - Enables authenticated mode when used together with `--session-id`.
- `--session-id` 
  - Value of the sessionid cookie.
  - Must be provided together with `--steam-login-secure`.
- `--request-delay-ms` 
  - Minimum delay between requests in milliseconds (rate limiting).
  - Helps avoid rate limits or IP bans.
  - Default: 0 (no delay).
- `--env-file` 
  - Path to a custom .env file.
  - If omitted, the default path **config/.env** is used.
  - CLI arguments always override values loaded from the env file.
- `--print-config-mode`
  - Used for debbuging.
  - Print the current configuration loaded and **exit**.
  - **Modes:** SAFE (won't display cookies), FULL, NONE.
- `--dry-run`
  - Used for debugging.
  - Simulates run of the program without actually doing any fetching
- `--no-dry-run`
  - Explicitly disables dry-run mode, if its enabled in config
  - Causes argument conflict if paired with **--dry-run**
- `--output-format`
  - Choices: json, csv, xml and text
  - Default: json
- `--output-file`
  - Default: None
  - If not spetified, output would be printed to console

**Note:** CLI arguments take precedence over environment variables.


**The script will:**
- Fetch all available comments from the profile (across multiple pages)
- Determine whether the user has comments enabled, disabled, or if it is unknown
- Print a summary and list all extracted comments

---

## Logging
Logging is enabled by default.

Format:
```
YYYY-MM-DD HH:MM:SS [LEVEL] message
```

**Levels:**
- CONFIG_LEVEL - config info
- INFO - normal execution
- DRY_RUN_LEVEL - dry run info
- WARNING - missing optional configuration (e.g. .env)
- ERROR - fatal configuration or runtime issues

---

## Exit Codes

- `0` – Successful execution
- `1` – Unexpected runtime error
- `2` – Steam request failed
- `3` – Pagination limit exceeded
- `4` – Configuration error
- `5` – CLI arguments conflict

---

## Project structure
```
steam-comments-scraper/
├── main.py
├── cli/
│   ├── config_print_mode.py
|   ├── exceptions.py
│   └── dry_run.py
├── config/
│   ├── .env           # optional, not committed
│   ├── env.py
│   └── exceptions.py
├── domain/
│   ├── scrape_result.py
│   ├── comment.py
│   └── comment_status.py
├── output/
|   ├── serializers/
|   |   ├── base.py
|   |   ├── csv_serializer.py
|   |   ├── json_serializer.py
|   |   ├── text_serializer.py
|   |   └── xml_serializer.py
|   ├── output_format.py
|   └── output_manager.py
├── parsing/
│   ├── comments.py
│   └── user.py
├── services/
│   └── comment_loader.py
├── steam_client/
│   ├── exceptions.py
│   ├── rate_limiter.py
│   └── steam_client.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Limitations
- Some data is only accessible with valid cookies (e.g. comment permissions).
- Even with valid cookies, if the provided account does not have permission to view or post comments on the target profile, the script will not be able to determine comment visibility.
- Profile comments must be public.
- Not intended for scraping multiple profiles or high-frequency automation (risk of IP ban).

---

## Security Notice

Authentication cookies grant access equivalent to a logged-in Steam session.

- Never commit cookies to version control
- Never share cookies publicly
- Use a secondary or low-privilege account if possible

Cookies provided to this tool are used solely for making HTTP requests to Steam Community pages and are not stored, logged, or transmitted elsewhere.

---

## Future plans
1. Implement asynch requests sending.
2. HTTP session reuse and retry policies.
3. Basic test suite for config and parsers.

---

## License
- This project is licensed under the MIT License. Use at your own risk. Not affiliated with or endorsed by Valve or Steam.
