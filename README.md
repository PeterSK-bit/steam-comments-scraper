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
```

Optional:
```
steamLoginSecure=YOUR_STEAM_LOGINSECURE_COOKIE
sessionid=YOUR_SESSIONID_COOKIE
MAX_PAGINATION_DEPTH=maximum_number_of_pages_the_program_will_run
request_delay_ms=minimal_time_space_between_requests
```

> To get the cookies, log in to Steam in your browser, open **Developer Tools (F12) > Application > Cookies**, and copy the values for __steamLoginSecure__ and __sessionid__.

**Notes:**
- Cookies are optional
- Without cookies, the scraper runs in restricted mode
- Missing `.env` file does not stop execution (a warning is logged)
- Default MAX_PAGINATION_DEPTH is set at 100.
- Default requrequest_delay_ms is set to 0.

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
  --env-file config/.env
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
- INFO – normal execution
- WARNING – missing optional configuration (e.g. .env)
- ERROR – fatal configuration or runtime issues

---

## Exit Codes

- `0` – Successful execution
- `1` – Unexpected runtime error
- `2` – Steam request failed
- `3` – Pagination limit exceeded
- `4` – Configuration error

---

## Project structure
```
steam-comments-scraper/
├── main.py
├── config/
│   ├── .env           # optional, not committed
│   ├── env.py
│   └── exceptions.py
├── domain/
│   ├── user.py
│   ├── comment.py
│   └── comment_status.py
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
1. Add support for configurable logging levels.
2. Improve logging message consistency.
3. Implement asynch requests sending.

---

## License
- This project is licensed under the MIT License. Use at your own risk. Not affiliated with or endorsed by Valve or Steam.
