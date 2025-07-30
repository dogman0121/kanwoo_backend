from typing import List
from pytils.translit import slugify

from app.api.adapters.manga_form_adapter import MangaFormDTO
from app.domain.entities.manga.manga import Manga
from app.domain.entities.user import User
from app.domain.services.manga.genre_service import MangaGenreService
from app.domain.services.manga.manga_poster_service import MangaPosterService
from app.domain.services.repository_service import RepositoryService
from app.domain.services.user_service import UserService
from app.infrastructure.repositories import SQLUserRepository
from app.infrastructure.repositories.storage import FileStoragePosterRepository


class MangaService(RepositoryService):
    def create_manga(self, user: User, data: MangaFormDTO, poster_repo: FileStoragePosterRepository,
                     user_repo: SQLUserRepository, genre_repo) -> Manga:
        slug = slugify(data.name.strip())

        user_service = UserService(user_repo)
        authors = [user_service.get_user_by_id(author_id) for author_id in data.authors]
        artists = [user_service.get_user_by_id(artist_id) for artist_id in data.artists]
        publishers = [user_service.get_user_by_id(publisher_id) for publisher_id in data.publishers]

        genre_service = MangaGenreService(poster_repo)

        manga = Manga(
            name=data.name,
            slug=slug,
            description=data.description,
            year=data.year,
            creator=user,
            authors=authors,
            artists=artists,
            publishers=publishers
        )

        try:
            manga = self.repository.create(manga)
        except:
            raise

        try:
            MangaPosterService(poster_repo).create_posters(manga, data.posters_order, data.new_posters)
        except:
            self.repository.delete(manga)
            raise

        return manga

    def get_verified_newest_manga(self) -> List[Manga]:
        return self.repository.get_newest(verified=True)

    def get_verified_most_viewed_manga(self) -> List[Manga]:
        return self.repository.get_most_viewed(verified=True)

    def get_popular_manga(self) -> List[Manga]:
        return self.repository.get_most_viewed(verified=True)

    def get_verified_random_manga(self) -> List[Manga]:
        return self.repository.get_random(verified=True)

    def get_ended_manga(self) -> List[Manga]:
        return self.repository.get_ended(verified=True)
