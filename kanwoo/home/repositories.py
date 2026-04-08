from sqlalchemy import select

from kanwoo.repositories import BaseRepository
from kanwoo.manga.models import Manga

class HomeRepository(BaseRepository):
    
    def get_featured_manga(self):
        featured_manga = self.db_session.execute(
            select(Manga)
            .filter(
                Manga.promo_background_uuid != None, 
                Manga.promo_logo_uuid != None,
                Manga.promo_name_uuid != None        
            )
        ).scalars().all()
        
        return featured_manga

    def get_newest_manga(self):
        return self.db_session.execute(
            select(Manga).order_by(Manga.created_at.desc()).limit(10)
        ).scalars().all()

    def get_ended_manga(self):
        return self.db_session.execute(
            select(Manga).order_by(Manga.type_id).limit(10)
        ).scalars().all()