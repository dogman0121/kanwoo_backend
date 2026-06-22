from typing import TYPE_CHECKING
import time
from kanwoo import db
from kanwoo.file_storage import FileStorage
from kanwoo.uuid import UUID
from kanwoo.image import ImageServiceFactory
from kanwoo.entity import File
from kanwoo.database import DBTransaction

from .repositories import ChapterRepository
from .models import Chapter, Page
from .dto import ChapterUpdateDTO
from .exceptions import ChapterNotFoundException, ChapterWithNumberAlreadyExists, ChapterDeleteNotAllowed, ChapterUpdateNotAllowed
from .permissions import ChapterPolicy

class ChapterPageService:

    def __init__(
            self, 
            file_storage: FileStorage, 
            image_service_factory: ImageServiceFactory, 
            chapter_repo: ChapterRepository
        ):
        self.file_storage = file_storage
        self.image_service_factory = image_service_factory
        self.chapter_repo = chapter_repo

    def __get_page_path(self, uuid, ext):
        return f"pages/{uuid}{ext}"

    def add_page(self, chapter, page_file, order):
        page_filename, _ = page_file.filename.rsplit(".", 1)
        page_uuid = UUID.generate_uuid()

        image_service = self.image_service_factory.create(page_file, output_format="WEBP")
        
        page_resized_file = image_service.resize((1280, 1000000))

        self.file_storage.save(page_resized_file, self.__get_page_path(page_uuid, ".webp"))
        
        page = Page(
            uuid=page_uuid,
            order = order,
            orig_filename = page_filename,
            path=self.__get_page_path(page_uuid, ".webp")
        )

        chapter.pages.append(page)

    def delete_page(self, page):
        self.chapter_repo.delete_page(page)

class ChapterService:

    def __init__(
            self, 
            db_transaction: DBTransaction,
            chapter_page_service: ChapterPageService, 
            chapter_repo: ChapterRepository,
            chapter_policy: ChapterPolicy
        ):
        self.chapter_repo = chapter_repo
        self.chapter_page_service = chapter_page_service
        self.chapter_policy = chapter_policy
        self.db_transaction = self.db_transaction

    def _delete_chapter(self, chapter: Chapter):
        self.chapter_repo.delete_chapter(chapter)

    def system_get_chapter_by_id(self, chapter_id):
        chapter = self.chapter_repo.get_chapter_by_id(chapter_id)

        if chapter is None:
            raise ChapterNotFoundException

        return chapter
    
    def user_get_chapter_by_id(self, profile, chapter_id, by_link=False):
        chapter = self.chapter_repo.user_get_chapter_by_id(profile.id, chapter_id)

        if chapter is None:
            raise ChapterNotFoundException

        return chapter

    def create_chapter(self, translation, data):
        try:
            chapter = Chapter(
                name=data.name,
                chapter=data.chapter,
                tome=data.tome,
                translation_id=translation.id,
                creator_id=self.profile.id
            )


            for page_file in data.pages:
                page_filename, _ = page_file.filename.rsplit(".", 1)

                page_order = data.pages_order.index(page_filename)

                self.chapter_page_service.add_page(chapter, page_file, page_order)

            self.chapter_repo.create_chapter(chapter)
            
            return chapter

        except ValueError as e:
            db.session.rollback()

    
    def user_get_translation_chapters(self, profile, translation):
        chapters = self.chapter_repo.get_translation_chapters(translation.id)

        return chapters
    
    def system_update_pages(self, chapter: Chapter, pages: list[File], pages_order: list[str]):
        with self.db_transaction:
            for existing_page in chapter.pages:
                try:
                    order = pages_order.index(existing_page.uuid)

                    existing_page.order = order
                except ValueError:
                    self.chapter_page_service.delete_page(existing_page)

            for new_page in pages:
                order = pages_order.index(new_page.filename)

                self.chapter_page_service.add_page(chapter, new_page, order)
    
    def user_create_translation_chapter(self, profile, translation, data):
        if self.chapter_repo.check_chapter_with_number(translation.id, data.chapter):
            raise ChapterWithNumberAlreadyExists

        chapter = Chapter(
            name = data.name,
            chapter = data.chapter,
            privacy_id = data.privacy,
            creator_id=profile.id,
            translation_id=translation.id
        )

        self.system_update_pages(chapter, data.pages, data.pages_order)

        return self.chapter_repo.create_chapter(chapter)
    
    def user_update_chapter(self, profile, chapter: Chapter, data: ChapterUpdateDTO):
        if not self.chapter_policy.can_edit(profile, chapter):
            raise ChapterUpdateNotAllowed
        if chapter.chapter != data.chapter and self.chapter_repo.check_chapter_with_number(chapter.translation_id, data.chapter):
            raise ChapterWithNumberAlreadyExists
        
        self.system_update_pages(chapter, data.pages, data.pages_order)

        updated_chapter = self.chapter_repo.update_chapter(chapter, {
            "name": data.name,
            "chapter": data.chapter,
            "privacy_id": data.privacy
        })

        return updated_chapter

    def system_delete_chapter(self, chapter: Chapter):
        self._delete_chapter(chapter)

    def user_delete_chapter(self, profile, chapter: Chapter):
        if self.chapter_policy.can_delete(profile, chapter):
            self.chapter_repo.delete_chapter(chapter)

        raise ChapterDeleteNotAllowed
        