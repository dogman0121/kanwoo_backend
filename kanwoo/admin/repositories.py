from sqlalchemy import select
from sqlalchemy.orm import joinedload

from kanwoo.repositories import BaseRepository
from kanwoo.manga.models import Manga

class AdminMangaRepository(BaseRepository):

    def get_manga_list(self, query=None, statuses=None):
        q = select(Manga).options(
            joinedload(Manga.moderation_history)
        )

        if query:
            q = q.filter(Manga.name.like(f"%{query}%"))

        if statuses:
            q = q.filter(Manga.moderation_status_type_id.in_(statuses))
        
        return self.db_session.execute(q).unique().scalars().all()
    
    def get_manga(self, manga_slug):
        return self.db_session.execute(select(Manga).filter_by(slug=manga_slug)).scalar()