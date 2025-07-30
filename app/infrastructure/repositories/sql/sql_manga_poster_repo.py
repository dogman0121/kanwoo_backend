from app.domain.entities.manga import Manga
from app.domain.entities.file.upload_file import UploadFile
from PIL import Image

from app.domain.entities.manga.manga_poster import MangaPoster
from app.domain.repositories.sql.manga_poster_repo import MangaPosterRepository
from app.infrastructure.models.manga import SQLMangaPoster
from app.infrastructure.databases import sqlalchemy_db as db

from uuid import uuid4

from app.infrastructure.services.uuid_service import UUIDService


class SQLMangaPosterRepository(MangaPosterRepository):
    @staticmethod
    def _to_entity(model: SQLMangaPoster) -> MangaPoster:
        return MangaPoster(
            uuid=model.uuid,
            order=model.order,
        )

    @staticmethod
    def get_by_uuid(uuid: str) -> MangaPoster:
        res = SQLMangaPoster.query.filter_by(uuid=uuid).first()

        return SQLMangaPosterRepository._to_entity(res) if res else None

    def create(self, manga_id: int, orig_filename, order: int) -> MangaPoster:
        poster = SQLMangaPoster(
            uuid=UUIDService.generate(),
            manga_id=manga_id,
            orig_filename=orig_filename,
            order=order
        )

        poster.save(db, commit=True)

        return self._to_entity(poster)

    def delete(self, poster: MangaPoster) -> None:
        poster = SQLMangaPoster.query.filter_by(uuid=poster.uuid)

        poster.is_deleted = True

        poster.save(db, commit=True)