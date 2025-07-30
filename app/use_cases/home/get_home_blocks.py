from app.domain.services.manga.manga_service import MangaService
from app.domain.entities.home_blocks import HomeBlocks

class GetHomeBlocksUseCase:
    def __init__(self, manga_repo):
        self.manga_repo = manga_repo

    def execute(self):
        manga_service = MangaService(self.manga_repo)

        newest_manga = manga_service.get_verified_newest_manga()
        ended_manga = manga_service.get_ended_manga()
        slides = manga_service.get_popular_manga()

        return HomeBlocks(
            newest=newest_manga,
            ended=ended_manga,
            most_viewed=newest_manga,
            slides=slides,
        )


