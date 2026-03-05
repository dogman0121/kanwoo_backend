from .dto import SearchMangaDTO
from .repositories import SearchRepository

class SearchService:

    def __init__(self, search_repo):
        self.search_repo = search_repo

    def user_search_manga(self, profile, dto: SearchMangaDTO):
        return self.search_repo.user_get_manga(
            profile.id if profile else None,
            query=dto.query,
            genres=dto.genres,
            types=dto.genres,
            statuses=dto.statuses,
            adults=dto.adults,
            year_from=dto.year_from,
            year_to=dto.year_to
        )

    