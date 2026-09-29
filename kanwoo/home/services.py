from kanwoo.reading_progress.services import ReadingProgressService

from .dto import HeroBlockDTO, HeroMangaDataDTO, HomeMapItemDTO
from .schemas import HeroBlockType
from .repositories import HomeRepository
from .entities import HomeBlockType

class HomeService:
    
    def __init__(
        self,
        reading_progress_service: ReadingProgressService,
        home_repo: HomeRepository
    ):
        self.rp_service = reading_progress_service
        self.home_repo = home_repo

    def user_get_home_map(self, actor):
        return [
            HomeMapItemDTO(
                type=HomeBlockType.HERO,
                hash="1",
                title="Главное"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.READING_PROGRESSES,
                hash="2",
                title="Продолжить чтение"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.MANGA_LIST,
                hash="3",
                title="Новинки"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.MANGA_LIST,
                hash="4",
                title="Завершенные"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.MANGA_LIST,
                hash="5",
                title="Самые просматриваемые"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.LAST_ADDED_CHAPTERS,
                hash=None,
                title="Обновления глав"
            )
        ]

    def user_get_block_by_hash(self, actor, hash):
        if hash == "1":
            hero_blocks = []
            
            for block in self.home_repo.get_featured_manga():
                hero_blocks.append(
                    HeroBlockDTO(
                        type=HeroBlockType.MANGA,
                        data=HeroMangaDataDTO(
                            slug=block.slug,
                            name=block.promo_name,
                            logo=block.promo_logo,
                            background=block.promo_background
                        )
                    )
                )
            return HomeBlockType.HERO, hero_blocks
        elif hash == "2":
            progresses = self.rp_service.user_get_progresses(actor)

            return HomeBlockType.READING_PROGRESSES, progresses
        elif hash == "3":
            manga_list = self.home_repo.get_newest_manga()

            return HomeBlockType.MANGA_LIST, manga_list
        elif hash == "4":
            manga_list = self.home_repo.get_ended_manga()

            return HomeBlockType.MANGA_LIST, manga_list
        elif hash == "5":
            manga_list = self.home_repo.get_most_viewed_manga()

            return HomeBlockType.MANGA_LIST, manga_list
        else:
            raise KeyError("Invalid hash")