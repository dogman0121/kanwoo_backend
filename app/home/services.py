from .dto import HeroBlockDTO, HeroMangaDataDTO
from .schemas import HeroBlockType

from ..manga.repositories import MangaRepository

class HomeService:
    def __init__(self, profile):
        self.profile = profile

    def get_hero_slider(self):
        manga = MangaRepository.get_featured(self)

        hero_blocks = []

        for m in manga:
            hero_blocks.append(
                HeroBlockDTO(
                    type=HeroBlockType.manga,
                    data=HeroMangaDataDTO(
                        name=m.promo_name,
                        logo=m.promo_logo,
                        background=m.promo_background
                    )
                )
            )

        return hero_blocks

    def get_newest_manga(self):
        manga = MangaRepository.get_newest()
        return manga

    def get_ended_manga(self):
        manga = MangaRepository.get_newest()
        return manga

    def get_featured_manga(self):
        manga = MangaRepository.get_newest()
        return manga

    def get_profile_history(self):
        pass

    def get_random_manga(self):
        manga = MangaRepository.get_newest()
        return manga