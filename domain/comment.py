from datetime import datetime


class Comment:
    def __init__(self, author_name: str, timestamp:int, text: str):
        self._author_name = author_name
        self._timestamp = timestamp
        self._text = text
    
    def comment_tone(self) -> str:
        lowered = self._text.lower()
        if any(rep in lowered for rep in ("-rep", "- rep", "rep-")): return "Negative"
        if any(rep in lowered for rep in ("+rep", "+ rep", "rep+")): return "Positive"
        return "Neutral"

    def __str__(self) -> str:
        return f"At {datetime.fromtimestamp(self._timestamp)} user named {self._author_name} commented: {self._text}"
    
    #getters
    @property
    def author_name(self) -> str:
        return self._author_name
    
    @property
    def timestamp(self) -> int:
        return self._timestamp
    
    @property
    def text(self) -> str:
        return self._text