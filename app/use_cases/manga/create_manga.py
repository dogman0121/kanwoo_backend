from app.api.adapters.manga_form_adapter import MangaFormDTO
from app.domain.entities.manga import Manga
from app.domain.entities.user import User
from app.domain.services.manga.manga_service import MangaService
from app.infrastructure.repositories import SQLMangaRepository
from app.infrastructure.repositories.storage import FileStoragePosterRepository


class CreateMangaUseCase:
    def __init__(self, manga_repository: SQLMangaRepository, poster_repository: FileStoragePosterRepository):
        self.manga_repository = manga_repository
        self.poster_repository = poster_repository

    def execute(self, user: User, data: MangaFormDTO) -> Manga:
        manga_service = MangaService(self.manga_repository)

        manga = manga_service.create_manga(user, data, self.poster_repository)

        return manga
