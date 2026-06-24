from .dto import HeroBlockDTO, HeroMangaDataDTO
from .schemas import HeroBlockType
from .repositories import HomeRepository

class HomeService:
    
    def __init__(self, home_repo: HomeRepository):
        self.home_repo = home_repo

    def user_get_hero_slides(self, profile):
        manga = self.home_repo.get_featured_manga()

        hero_blocks = []

        for m in manga:
            hero_blocks.append(
                HeroBlockDTO(
                    type=HeroBlockType.manga,
                    data=HeroMangaDataDTO(
                        slug=m.slug,
                        name=m.promo_name,
                        logo=m.promo_logo,
                        background=m.promo_background
                    )
                )
            )

        return hero_blocks
    
    def user_get_most_viewed_manga(self, profile):
        manga = self.home_repo.get_most_viewed_manga()

        return manga

    def user_get_newest_manga(self, profile):
        manga = self.home_repo.get_newest_manga()
        return manga

    def user_get_ended_manga(self, profile):
        manga = self.home_repo.get_newest_manga()
        return manga