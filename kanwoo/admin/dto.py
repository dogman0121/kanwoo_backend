from dataclasses import dataclass
from typing import List

@dataclass
class MainDashboardDTO:
    manga_reports_count: int
    chapters_reports_count: int
    manga_waiting_moderation_count: int
    chapter_waiting_moderation_count: int
    manga_sugesstions_count: int
    feedback_messages_count: int


@dataclass
class MangaFiltersDTO:
    query: str
    statuses: List[str]