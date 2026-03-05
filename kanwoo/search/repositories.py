from typing import Optional
from sqlalchemy import exists, select

from kanwoo.repositories import BaseRepository
from kanwoo.manga.models import Manga, manga_genres

class SearchRepository(BaseRepository):
    def user_get_manga(self, profile_id: Optional[int], query, genres=None, types=None, statuses=None, adults=None, year_from=None, year_to=None):
        orm_query = select(Manga)

        if genres:
            orm_query = orm_query.filter(
                exists(
                    select(manga_genres.c.genre_id)
                    .where(manga_genres.c.manga_id == Manga.id)
                ).where(manga_genres.c.genre_id.in_(genres) == True)
            )

        if types:
            orm_query = orm_query.filter(
                exists().where(Manga.type_id.in_(types))
            )

        if statuses:
            orm_query = orm_query.filter(
                exists().where(Manga.status_id.in_(statuses))
            )

        if adults:
            orm_query = orm_query.filter(
                exists().where(Manga.adult_id.in_(adults))
            )

        if year_from:
            orm_query = orm_query.filter(
                Manga.year >= year_from
            )
        
        if year_to:
            orm_query = orm_query.filter(
                Manga.year <= year_to
            )

        if query:
            orm_query = orm_query.filter(Manga.name.like(f"%{query}%"))

        return self.db_session.execute(orm_query.filter(Manga.can_view(profile_id)==True)).scalars().all()