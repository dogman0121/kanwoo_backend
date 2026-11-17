from .dto import SearchMangaDTO
from .repositories import SearchRepository

class SearchService:

    def __init__(self, search_repo: SearchRepository):
        self.search_repo = search_repo

    def search_manga(self, search_dto: SearchMangaDTO, page, per_page):

        results, total_count =  self.search_repo.search_manga(
            page,
            per_page,
            query=search_dto.query,
            genres=search_dto.genres,
            types=search_dto.genres,
            statuses=search_dto.statuses,
            adults=search_dto.adults,
            year_from=search_dto.year_from,
            year_to=search_dto.year_to,
        )

        return results, total_count

    