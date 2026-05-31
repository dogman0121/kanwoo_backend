from typing import Optional
from sqlalchemy import exists, select, func

from kanwoo.models import page_paginate
from kanwoo.repositories import BaseRepository
from kanwoo.manga.models import Manga, manga_genres

class SearchRepository(BaseRepository):
    def user_search_manga(self, profile_id: Optional[int], page: int, per_page: int, query: str = None, genres=None, types=None, statuses=None, adults=None, year_from=None, year_to=None):
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
            orm_query = orm_query.filter(func.lower(Manga.name).like(f"%{query.lower()}%"))


        results, total_count = page_paginate(self.db_session, orm_query, page, per_page)

        return results, total_count