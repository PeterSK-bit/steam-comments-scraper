from bs4 import BeautifulSoup

class UserParser:
    @staticmethod
    def parse_user(html: bytes) -> str | None:
        if not html: return None
        
        soup = BeautifulSoup(html, "html.parser")
        user_info = soup.find("div", class_="profile_small_header_text")

        if not user_info: return None

        username = user_info.find("a", class_="persona_name_text_content").text.strip()
        return username