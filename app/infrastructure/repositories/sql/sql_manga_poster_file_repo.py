from app.domain.entities.manga.manga_poster import MangaPoster
from app.domain.entities.manga.manga_poster_file import MangaPosterFile
from app.domain.repositories.sql.manga_poster_file_repo import MangaPosterFileRepository
from app.infrastructure.models.manga.sql_manga_poster_file import SQLMangaPosterFile
from app.infrastructure.databases.sql_alchemy import sqlalchemy_db


class SQLMangaPosterFileRepository(MangaPosterFileRepository):
    @staticmethod
    def _to_entity(model: SQLMangaPosterFile) -> MangaPosterFile:
        return MangaPosterFile(
            uuid=model.uuid,
            type=model.type,
        )

    def create(self, poster_uuid: str, file_type: str, file_uuid: str) -> MangaPosterFile:
        poster_file = SQLMangaPosterFile(
            uuid=file_uuid,
            poster_uuid=poster_uuid,
            type=file_type,
        )

        poster_file.save(sqlalchemy_db, commit=True)

        return self._to_entity(poster_file)