from kanwoo.reading_progress.services import ReadingProgressService

from kanwoo.manga.services import MangaStatsService
from kanwoo.chapter.services import ChapterService
from .dto import HeroBlockDTO, HeroMangaDataDTO, HomeMapItemDTO, LastAddedChaptersDTO, ReadingProgressDTO
from .schemas import HeroBlockType
from .entities import HomeBlockType

class HomeService:
    
    def __init__(
        self,
        reading_progress_service: ReadingProgressService,
        chapter_service: ChapterService,
        manga_stats_service: MangaStatsService
    ):
        self.rp_service = reading_progress_service
        self.chapter_service = chapter_service
        self.manga_stats_service = manga_stats_service

    def user_get_home_map(self, actor):
        return [
            HomeMapItemDTO(
                type=HomeBlockType.HERO,
                hash="hero",
                title="Главное"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.READING_PROGRESSES,
                hash="reading-progresses",
                title="Продолжить чтение"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.MANGA_LIST,
                hash="newest",
                title="Новинки"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.MANGA_LIST,
                hash="ended",
                title="Завершенные"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.MANGA_LIST,
                hash="most-viewed",
                title="Самые просматриваемые"
            ),
            HomeMapItemDTO(
                type=HomeBlockType.LAST_ADDED_CHAPTERS,
                hash="last-added-chapters",
                title="Обновления глав"
            )
        ]

    def user_get_block_by_hash(self, actor, hash):
        if hash == "hero":
            hero_blocks = []
            
            for block in self.manga_stats_service.user_get_manga_with_promo():
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
        elif hash == "reading-progresses":
            progresses = self.rp_service.user_get_progresses(actor)

            res = []
            for prog in progresses:
                res.append(
                    ReadingProgressDTO(
                        id=prog.id,
                        page=prog.page,
                        chapter=prog.chapter,
                        manga=prog.manga
                    )
                )

            return HomeBlockType.READING_PROGRESSES, res
        elif hash == "newest":
            return HomeBlockType.MANGA_LIST, self.manga_stats_service.user_get_newest_manga()
        elif hash == "ended":
            return HomeBlockType.MANGA_LIST, self.manga_stats_service.user_get_ended_manga()
        elif hash == "most-viewed":
            return HomeBlockType.MANGA_LIST, self.manga_stats_service.user_get_most_viewed_manga()
        elif hash == "last-added-chapters":
            chapters, cursor, has_more = self.chapter_service.user_get_last_added_chapters(actor, None)
            
            return HomeBlockType.LAST_ADDED_CHAPTERS, LastAddedChaptersDTO(
                chapters=chapters,
                pagination={
                    "cursor": cursor,
                    "has_more": has_more
                }
            )
        else:
            raise KeyError("Invalid hash")