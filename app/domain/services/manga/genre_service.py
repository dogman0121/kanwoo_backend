from app.domain.services.repository_service import RepositoryService


class MangaGenreService(RepositoryService):
    def get_by_genre_id(self, genre_id):
        return self.repository.get_by_id(genre_id)