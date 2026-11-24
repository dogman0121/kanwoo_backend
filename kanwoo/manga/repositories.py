from sqlalchemy import func, select, or_, update, insert
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.dialects.postgresql import insert as psql_insert

from kanwoo.entities import Privacy
from kanwoo.moderation.entity import ModerationStatus
from kanwoo.repositories import BaseRepository
from kanwoo.comment.models import MangaComment
from kanwoo.collection.models import CollectionManga
from .models import Manga, MangaSuggestion, Genre, MangaView

class MangaRepository(BaseRepository):

    def get_all(self):
        pass

    def get_manga_by_slug(self, slug: str, public: bool = True):
        stmt = (select(Manga)
            .where(
                Manga.slug == slug,
            )
        )

        if public:
            stmt = stmt.where(
                or_(
                    Manga.privacy_id == Privacy.PUBLIC.value,
                    Manga.privacy_id == Privacy.BY_LINK.value
                ),
                Manga.moderation_status_type_id == ModerationStatus.APPROVED.value
            )

        stmt = stmt.options(
            joinedload(Manga.poster),   
            joinedload(Manga.background),    
            joinedload(Manga.type),
            joinedload(Manga.status),
            joinedload(Manga.adult),
            joinedload(Manga.author),
            selectinload(Manga.name_translations),
            selectinload(Manga.genres)
        )

        return self.db_session.execute(stmt).scalar_one_or_none()

    def get_manga_by_id_from_user(self, profile, manga_id):
        return self.db_session.execute(
            select(Manga)
            .filter(
                Manga.id==manga_id,
                Manga.can_view(profile)==True
            )).scalar()
    
    def get_manga_by_slug_from_user(self, profile, manga_slug, by_link=False):
        return self.db_session.execute(
            select(Manga)
            .filter(
                Manga.slug==manga_slug,
                Manga.can_view(profile, by_link)
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


    def get_profile_manga(self, actor, profile_id: int):
        return self.db_session.execute(
            select(Manga).filter(
                Manga.creator_id==profile_id,
                Manga.can_view(actor)==True
            )
        ).scalars().all()

    def get_genres_by_ids(self, genres_ids):
        return self.db_session.execute(select(Genre).filter(Genre.id.in_(genres_ids))).scalars().all()
    

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

class MangaStatsRepository(BaseRepository):
    
    def get_manga_with_promo(self):
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
    
    def get_most_viewed_manga(self):
        return self.db_session.execute(
            select(Manga)
            .join(MangaView, Manga.id == MangaView.manga_id).order_by(MangaView.views).limit(10)
        ).scalars().all()

class MangaStatRepository(BaseRepository):

    def get_views(self, manga_slug: str) -> int:
        stmt = (
            select(MangaView.views)
            .join(Manga, Manga.id == MangaView.manga_id)
            .where(
                Manga.slug == manga_slug,
            )
        )

        return self.db_session.execute(stmt).scalar_one_or_none()

    def add_view(self, manga_slug: str):
        manga_id = (
            select(Manga.id)
            .where(Manga.slug == manga_slug)
            .scalar_subquery()
        )

        stmt = psql_insert(MangaView).values(
            manga_id = manga_id,
            views = 1
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[MangaView.manga_id],
            set_={"views": MangaView.views + 1}
        )

        self.db_session.execute(stmt)

    def get_comments(self, manga_slug):
        stmt = (
            select(func.count(""))
            .select_from(MangaComment)
            .join(Manga, MangaComment.manga_id == Manga.id)
            .where(Manga.slug == manga_slug)
        )

        return self.db_session.execute(stmt).scalar_one_or_none()

    def get_saves(self, manga_slug):
        stmt = (
            select(func.count(CollectionManga.collection_id))
            .join(Manga, Manga.id == CollectionManga.manga_id)
            .where(
                Manga.slug == manga_slug
            )
        )

        return self.db_session.execute(stmt).scalar_one_or_none()