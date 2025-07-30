from typing import Tuple, Dict

from app.domain.entities.file.upload_file import UploadFile
from app.domain.entities.manga import Manga
from app.domain.orchestration.file_orchestrator import FileOrchestratorAction
from app.infrastructure.repositories.sql.sql_manga_poster_file_repo import SQLMangaPosterFileRepository
from app.infrastructure.repositories.sql.sql_manga_poster_repo import SQLMangaPosterRepository
from app.infrastructure.repositories.storage.storage_manga_poster_file import LocalMangaPosterFileStorage


class MangaPosterOrchestrationAction(FileOrchestratorAction):
    def __init__(self, poster_repo: SQLMangaPosterRepository,
                 poster_file_storage: LocalMangaPosterFileStorage,
                 poster_file_repo: SQLMangaPosterFileRepository,
                 poster_uuid, poster_file: UploadFile, order: int,
                 manga: Manga, sizes: Dict[str, Tuple[int, int]]
                 ):
        self.poster_repo = poster_repo
        self.poster_file_storage = poster_file_storage
        self.poster_file_repo = poster_file_repo
        self.poster_uuid = poster_uuid
        self.poster_file = poster_file
        self.manga = manga
        self.sizes = sizes
        self.order = order
        self.poster = None


    def save(self):
        poster = self.poster_repo.create(
            manga_id=self.manga.id,
            orig_filename=self.poster_file.filename,
            order=self.order
        )
        self.poster = poster

        for size_name, size in self.sizes.items():
            poster_file_uuid = self.poster_file_storage.save(
                manga=self.manga,
                poster_file=self.poster_file,
                poster_size=size,
            )

            poster_file = self.poster_file_repo.create(
                poster_uuid=poster.uuid,
                file_type=size_name,
                file_uuid=poster_file_uuid,
            )

    def delete(self):
        if self.poster is not None:
            self.poster_repo.delete(self.poster)