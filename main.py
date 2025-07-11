from requests import get
from bs4 import BeautifulSoup
from classes import Comment, User, CommentStatus

def main():
    #loading env file
    env_vars = {}
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            env_vars[key] = value

    MAX_PAGINATION_DEPTH = int(env_vars.get("MAX_PAGINATION_DEPTH", 100))

    #setting up steam url
    steam_url = env_vars["steam_url"] if "steam_url" in env_vars else input(
        'STATUS: .env file is missing steam_url, enter it manually or add it to .env and type "restart"\nInput: ')
    
    if steam_url == "restart": return main()
    if not steam_url.endswith("/allcomments"): steam_url += "/allcomments"

    #setting up cookies
    cookies_enabled = True
    for key in ["steamLoginSecure", "sessionid"]:
        val = env_vars.get(key, "").strip()
        if not val:
            print(f"WARNING: Missing or empty cookie key: {key}")
            cookies_enabled = False
    
    if not cookies_enabled:
        print("WARING: Without proper session it's impossible to get some data.")

    cookies = {
        'steamLoginSecure': env_vars["steamLoginSecure"],
        'sessionid': env_vars["sessionid"]
    } if cookies_enabled else None

    #pagination
    page = 1
    extracted_comments = []

    while True:
        #getting html
        response = get(f"{steam_url}?ctp={page}", cookies=cookies)

        if response.status_code != 200:
            print(f"ERROR: Unable to get site, status code -> {response.status_code}")
            break
        
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
    #user.print_account_comments()

if __name__ == "__main__":
    main()