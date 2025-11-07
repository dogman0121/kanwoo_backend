from .models import Manga

class MangaRepository:

    def get_all(self):
        pass

    def create_manga(self, manga: Manga):
        manga.add()

        return manga
    
    def delete_poster(self, manga: Manga):
        poster = manga.poster
        if poster is None:
            return

        poster.is_deleted = True
        for poster_file in poster.files:
            poster_file.is_deleted = True
        
        manga.poster = None

    def set_poster(self, manga: Manga, poster):
        if manga.poster:
            self.delete_poster(manga)
        
        manga.poster = poster

    def get_by_id(self, manga_id):
        return Manga.query.filter_by(id=manga_id).scalar()
    
    def get_by_slug(self, manga_slug):
        return Manga.query.filter_by(slug=manga_slug).scalar()

    def get_featured(self):
        featured_manga = Manga.query.filter_by(is_featured=True).all()
        
        return featured_manga

    @staticmethod
    def get_newest():
        return (
            Manga.query.order_by(Manga.created_at.desc()).limit(10).all()
        )

    @staticmethod
    def get_ended():
        return (
            Manga.query.order_by(Manga.type_id).limit(10).all()
        )
