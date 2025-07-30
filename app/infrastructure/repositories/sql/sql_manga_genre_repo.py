from app.domain.repositories.sql.manga_genre_repo import MangaGenreRepository
from app.domain.entities.manga.manga_genre import MangaGenre
from app.infrastructure.models.manga.sql_manga_genre import SQLMangaGenre


class SQLMangaGenreRepository(MangaGenreRepository):
    @staticmethod
    def _to_entity(model: SQLMangaGenre):
        return MangaGenre(
            id=model.id,
            name=model.name
        )


    def get_by_id(self, genre_id):
        res = SQLMangaGenre.query.filter_by(id=genre_id).first()

        return self._to_entity(res) if res else None