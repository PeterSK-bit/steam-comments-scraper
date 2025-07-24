from requests import get, exceptions
import sys
from bs4 import BeautifulSoup
from classes import Comment, User, CommentStatus

def load_env() -> dict:
    env_vars = {}
    
    try:
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                env_vars[key] = value
        return env_vars
    except FileNotFoundError:
        print("ERROR: .env file not found, program will run in restricted mode.")
        return {}
    except Exception as e:
        print(f"ERROR: Failed to read .env file -> {e}")
        return {}

def main() -> int:
    env_vars = load_env()

    try:
        MAX_PAGINATION_DEPTH = int(env_vars.get("MAX_PAGINATION_DEPTH", 100))
    except ValueError:
        print("WARNING: MAX_PAGINATION_DEPTH is not a valid integer, defaulting to 100")
        MAX_PAGINATION_DEPTH = 100

    #setting up steam url
    steam_url = env_vars["steam_url"] if "steam_url" in env_vars else input(
        'STATUS: .env file is missing steam_url, enter it manually or add it to .env and type "restart"\nInput: ')
    
    if steam_url == "restart": return main()
    if not steam_url.endswith("/allcomments"): steam_url += "/allcomments"

    #setting up cookies
    cookies_enabled = True
    missing = []
    for key in ["steamLoginSecure", "sessionid"]:
        val = env_vars.get(key, "").strip()
        if not val:
            missing.append(key)
            cookies_enabled = False
    
    if not cookies_enabled:
        print(f"WARNING: Missing or empty cookie keys: {', '.join(missing)}")
        print("WARNING: Without proper session it's impossible to get some data.")

    cookies = {
        'steamLoginSecure': env_vars["steamLoginSecure"],
        'sessionid': env_vars["sessionid"]
    } if cookies_enabled else None

    #pagination
    page = 1
    extracted_comments = []

    while True:
        try:
            response = get(f"{steam_url}?ctp={page}", cookies=cookies)
            response.raise_for_status()
        except exceptions.HTTPError as e:
            print(f"ERROR: HTTP error occurred -> {e}")
            return 1
        except exceptions.RequestException as e:
            print(f"ERROR: Request failed -> {e}")
            return 1
        except Exception as e:
            print(f"ERROR: Unexpected error occurred -> {e}")
            return 1
        
        #parsing html
        soup = BeautifulSoup(response.content, "html.parser")

        #extracting comments
        comment_entry = soup.find("div", class_="commentthread_entry_quotebox")
        comments = soup.find_all("div", class_="commentthread_comment")
        if not comments:
            print("STATUS: All comments loaded")
            break

        for comment in comments:
            author = comment.find("a", class_="commentthread_author_link").text.strip()
            timestamp = int(comment.find("span", class_="commentthread_comment_timestamp")["data-timestamp"])
            text = comment.find("div", class_="commentthread_comment_text").text.strip()
            extracted_comments.append(Comment(author, timestamp, text))
        
        if page >= MAX_PAGINATION_DEPTH:
            print(f"STATUS: Emergency break, max pagination depth of {MAX_PAGINATION_DEPTH} pages reached, not all comments might have loaded.")
            break
        
        page += 1

    if not cookies_enabled:
        comment_status = CommentStatus.UNKNOWN
    else:
        comment_status = CommentStatus.ENABLED if comment_entry else CommentStatus.DISABLED

    user = User(soup.find("a", class_="persona_name_text_content").text.strip(), extracted_comments, comment_status)

    print(user)
    user.print_account_comments()
    
    return 0

if __name__ == "__main__":
    result = main()
    print("INFO: Program ran successfully" if result == 0 else "INFO: Program crashed")
    sys.exit(result) 