from app.domain.entities.manga import Manga
from app.domain.entities.file.upload_file import UploadFile
from app.domain.entities.manga.manga_poster import MangaPoster
from app.domain.orchestration.file_orchestrator import FileOrchestrator
from app.domain.orchestration.manga_poster_orchestrator_action import MangaPosterOrchestrationAction
from app.domain.services.repository_service import RepositoryService

from typing import List

from app.infrastructure.repositories.sql.sql_manga_poster_file_repo import SQLMangaPosterFileRepository
from app.infrastructure.repositories.storage.storage_manga_poster_file import LocalMangaPosterFileStorage


class MangaPosterService(RepositoryService):
    sizes = {
        "thumbnail": (80, 120),
        "small": (200, 300),
        "medium": (400, 600),
        "large": (800, 1200)
    }

    def create_posters(self, poster_file_repository: SQLMangaPosterFileRepository,
                       poster_file_storage: LocalMangaPosterFileStorage, manga: Manga,
                       poster_files: List[UploadFile]):
        orchestrator = FileOrchestrator()

        for order, poster_file in enumerate(poster_files):
            action = MangaPosterOrchestrationAction(
                poster_repo=self.repository,
                poster_file_storage=poster_file_storage,
                poster_file_repo=poster_file_repository,
                manga=manga,
                poster_file=poster_file,
                sizes=self.sizes,
                order=order
            )

            orchestrator.add_action(action)

        try:
            orchestrator.execute()
        except Exception:
            raise

    def update_posters(self, posters_order, new_posters: List[UploadFile]):
        pass

    @staticmethod
    def get_file_link(poster_file_storage: LocalMangaPosterFileStorage, manga: Manga, poster_uuid: str):
        return poster_file_storage.get_link(manga_id=manga.id, file_uuid=poster_uuid)

    def get_posters(self, poster_file_repository: SQLMangaPosterFileRepository, manga: Manga) -> List[MangaPoster]:
        posters = self.repository.get_manga_posters(manga)

        for poster in posters:
            poster_versions = poster_file_repository.get_versions(poster.uuid)

            for poster_version in poster_versions:
                if poster_version.type == "thumbnail":
                    poster.thumbnail = poster_version
                elif poster_version.type == "small":
                    poster.small = poster_version
                elif poster_version.type == "medium":
                    poster.medium = poster_version
                elif poster_version.type == "large":
                    poster.large = poster_version

        return posters
