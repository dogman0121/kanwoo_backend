from sqlalchemy import select, exists

from kanwoo.repositories import BaseRepository

from .models import Chapter, Page

class ChapterRepository(BaseRepository):

    def system_get_chapter_by_id(self, chapter_id):
        return self.db_session.execute(select(Chapter).filter_by(chapter_id)).scalar()

    def user_get_chapter_by_id(self, profile_id, chapter_id, by_link=False):
        return self.db_session.execute(
            select(Chapter)
            .filter(
                Chapter.id == chapter_id, 
                Chapter.can_view(profile_id, by_link) == True
            )
        ).scalar()

    def get_translation_chapters(self, translation_id):
        return self.db_session.execute(
            select(Chapter)
            .filter_by(
                translation_id=translation_id
            )
            .order_by(Chapter.chapter.desc())
        ).scalars().all()
    
    def check_chapter_with_number(self, translation_id, chapter_number):
        return self.db_session.execute(select(exists(Chapter).where(
            Chapter.translation_id==translation_id, 
            Chapter.chapter==chapter_number,
        ))).scalar()
    
    def create_chapter(self, chapter: Chapter):
        chapter.add(commit=True)

        return chapter
    
    def update_chapter(self, chapter: Chapter, data: dict):
        chapter.update(data, commit=True)

        return chapter
    
    def delete_page(self, page: Page):
        page.is_deleted = True

    def create_page(self, chapter: Chapter, page: Page):
        chapter.pages.append(page)

    def delete_chapter(self, chapter: Chapter):
        for p in chapter.pages:
            p.is_deleted = True
            
        chapter.delete()
