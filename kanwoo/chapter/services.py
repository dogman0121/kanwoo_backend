from app import db, storage
from app.uuid import UUID
from app.image import ImageService

from .models import Chapter, Page
from .dto import ChapterCreateDTO
from .exceptions import ChapterNotFoundException

class ChapterService:
    def __init__(self, profile):
        self.profile = profile

    @staticmethod
    def get_chapter_by_id(chapter_id):
        chapter = Chapter.query.filter_by(id=chapter_id).scalar()

        if chapter is None:
            raise ChapterNotFoundException

        return chapter

    def create_chapter(self, translation, data: ChapterCreateDTO):
        try:
            pages = []

            for page_file in data.pages:
                page_filename, ext = page_file.filename.rsplit(".", 1)
                page_order = data.pages_order.index(page_filename)
                page_uuid = UUID.generate_uuid()

                page = Page(
                    uuid=page_uuid,
                    order = page_order,
                    ext=".webp"
                )

                page_image = ImageService(page_file, output_format="WEBP").resize((1280, 1000000))
                storage.save(page_image, f"pages/{page_uuid}.webp")

                pages.append(page)

            chapter = Chapter(
                name=data.name,
                chapter=data.chapter,
                tome=data.tome,
                pages=pages,
                creator_id=self.profile.id
            )

            translation.chapters.append(chapter)

            db.session.commit()
            
            return chapter

        except ValueError as e:
            print(e)
            db.session.rollback()

    