from enum import Enum

class HeroBlockType(Enum):
    MANGA = "manga"


class HomeBlockType(Enum):
    HERO = "hero"
    READING_PROGRESSES = "reading_progresses"
    MANGA_LIST = "manga_list"
    LAST_ADDED_CHAPTERS = "last_added_chapters"