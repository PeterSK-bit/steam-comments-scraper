from dataclasses import dataclass

@dataclass(frozen=True)
class Comment:
    author_name: str
    timestamp: int
    text: str