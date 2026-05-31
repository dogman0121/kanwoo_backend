from sqlalchemy import select
from sqlalchemy.orm import joinedload

from kanwoo.repositories import BaseRepository
from kanwoo.manga.models import Manga
from kanwoo.profile.models import Profile
from kanwoo.models import page_paginate

class AdminMangaRepository(BaseRepository):

    def get_manga_list(self, page, per_page, query=None, statuses=None):
        q = select(Manga).options(
            joinedload(Manga.moderation_history)
        )

        if query:
            q = q.filter(Manga.name.like(f"%{query}%"))

        if statuses:
            q = q.filter(Manga.moderation_status_type_id.in_(statuses))
        
        results, total_count = page_paginate(self.db_session, q.order_by(Manga.created_at), page, per_page)
        
        return results, total_count 
    
    def get_manga(self, manga_slug):
        return self.db_session.execute(select(Manga).filter_by(slug=manga_slug)).scalar()
    

class AdminProfileRepository(BaseRepository):
    
    def get_profiles_list(self, page, per_page, query=None):
        q = select(Profile)

        if query:
            q = q.filter(Profile.name.like(f"%{query}%"))
        
        result, total_count = page_paginate(self.db_session, q.order_by(Profile.created_at), page, per_page)

        return result, total_count