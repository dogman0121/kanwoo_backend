from .models import Manga

class MangaRepository:

    @staticmethod
    def create_manga(manga: Manga):
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


    @staticmethod
    def get_all():
        pass

    @staticmethod
    def get_by_id(manga_id):
        return Manga.query.filter_by(id=manga_id).scalar()
    
    @staticmethod
    def get_by_slug(manga_slug):
        return Manga.query.filter_by(slug=manga_slug).scalar()

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
