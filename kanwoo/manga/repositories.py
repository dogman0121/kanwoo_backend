from sqlalchemy import func, select, exists

from kanwoo.repositories import BaseRepository

from .models import Manga, MangaSuggestion, Genre

class MangaRepository(BaseRepository):

    def get_all(self):
        pass

    def get_manga_by_id_from_user(self, profile_id, manga_id):
        return self.db_session.execute(
            select(Manga)
            .filter(
                Manga.id==manga_id,
                Manga.can_view(profile_id)==True
            )).scalar()
    
    def get_manga_by_slug_from_user(self, profile_id, manga_slug, by_link=False):
        return self.db_session.execute(
            select(Manga)
            .filter(
                Manga.slug==manga_slug,
                Manga.can_view(profile_id, by_link)
            )).scalar()
    
    def get_manga_by_slug_from_system(self, manga_slug):
        return self.db_session.execute(select(Manga).filter_by(slug=manga_slug)).scalar()
    
    def check_if_genres_exists(self, genres_ids: list[int]):
        match_count =  self.db_session.execute(
            select(func.count(Genre.id).filter(Genre.id.in_(genres_ids)))
        ).scalar()

        return match_count == len(genres_ids)
    

    def create_manga(self, manga: Manga):
        manga.add()

        return manga
    
    def update_manga(self, manga: Manga, data: dict):
        manga.update(data, commit=False)
        
        return manga

    def delete_manga(self, manga: Manga):
        manga.delete(commit=True)

    def delete_poster(self, manga: Manga):
        if manga.poster:
            manga.poster.delete()

    def set_poster(self, manga: Manga, poster):
        if manga.poster:
            self.delete_poster(manga)

        manga.poster = poster

    def set_background(self, manga: Manga, background):
        if manga.background:
            manga.background.delete()

        manga.background = background

    def set_promo_name(self, manga: Manga, promo_name):
        if manga.promo_name:
            manga.promo_name.delete()

        manga.promo_name = promo_name

    def set_promo_logo(self, manga: Manga, promo_logo):
        if manga.promo_logo:
            manga.promo_logo.delete()

        manga.promo_logo = promo_logo

    def set_promo_background(self, manga: Manga, promo_background):
        if manga.promo_background:
            manga.promo_background.delete()

        manga.promo_background = promo_background

    def delete_background(self, manga):
        if manga.background:
            manga.background.delete()

    def delete_promo_name(self, manga):
        if manga.promo_name:
            manga.promo_name.delete()

    def delete_promo_logo(self, manga):
        if manga.promo_logo:
            manga.promo_logo.delete()

    def delete_promo_background(self, manga):
        if manga.promo_background:
            manga.promo_background.delete()

    def save_manga(self, manga):
        manga.save()
        return manga


    def get_profile_manga(self, current_profile_id, profile_id: int):
        return self.db_session.execute(
            select(Manga).filter(
                Manga.creator_id==profile_id,
                Manga.can_view(profile_id)==True
            )
        ).scalars().all()
    

class MangaSuggestionRepository(BaseRepository):
    def create_suggestion(self, suggestion):
        suggestion.add(commit=True)

        return suggestion
    
    def update_suggestion(self, suggestion, data):
        suggestion.update(data, commit=True)

        return suggestion

    def get_suggestion_by_id(self, suggestion_id):
        return self.db_session.execute(select(MangaSuggestion).filter(MangaSuggestion.id==suggestion_id)).scalar()

    def get_suggestions(self, resolved = None):
        q  = select(MangaSuggestion)
        
        if resolved is None:
            pass
        else:
            if resolved:
                q = q.filter(MangaSuggestion.resolved_at.isnot(None))
            else:
                q = q.filter(MangaSuggestion.resolved_at.is_(None))

        return self.db_session.execute(q.order_by(MangaSuggestion.created_at)).scalars().all()


    def get_active_suggestions_count(self):
        return self.db_session.execute(
            select(func.count("*"))
            .where(MangaSuggestion.resolved_at == None)
        ).scalar()