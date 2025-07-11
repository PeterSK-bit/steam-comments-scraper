# Steam comments scraper
A Python script that scrapes public comments from a Steam Community profile, with support for pagination, comment visibility detection, and both authenticated (via cookies) and unauthenticated modes.

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

## Environment Configuration
Create a **.env** file in the root of the project with the following structure:
```
steam_url=https://steamcommunity.com/id/yourSteamID
steamLoginSecure=YOUR_STEAM_LOGINSECURE_COOKIE
sessionid=YOUR_SESSIONID_COOKIE
```

> If you don't provide cookies, the script will still run in limited mode, but comment visibility status will be unavailable.
> To get the cookies, log in to Steam in your browser, open **Developer Tools (F12) > Application > Cookies**, and copy the values for __steamLoginSecure__ and __sessionid__.

Optional:
```
MAX_PAGINATION_DEPTH=maximum_number_of_pages_the_program_will_run
```

## Run script
```
python main.py
```

The script will:
- Fetch all available comments from the profile (across multiple pages)
- Determine whether the user has comments enabled, disabled, or if it is unknown
- Print a summary and list all extracted comments

## Project structure
```
steam-comments-scraper/
├── main.py              # Main script
├── classes.py           # User, Comment, and CommentStatus classes
├── .env                 # Your local environment variables (not committed)
├── .gitignore
```

## Limitations
- Some data is only accessible with valid cookies (e.g. comment permissions).
- Even with valid cookies, if the provided account does not have permission to view or post comments on the target profile, the script will not be able to determine comment visibility.
- Profile comments must be public.
- Not intended for scraping multiple profiles or high-frequency automation (risk of IP ban).

## License
- This project is licensed under the MIT License. Use at your own risk. Not affiliated with or endorsed by Valve or Steam.
