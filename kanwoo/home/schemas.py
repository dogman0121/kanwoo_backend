from marshmallow import Schema, fields, pre_dump
from collections.abc import Sequence

from kanwoo.manga.schemas import GetMangaSchemaMini
from kanwoo.chapter.schemas import GetChapterSchemaMini
from .entities import HeroBlockType, HomeBlockType
from .dto import HeroBlockDTO, ReadingProgressDTO

class GetHeroBlockData(Schema):
    pass

class GetHeroBlockManga(GetHeroBlockData):
    slug = fields.String()
    logo = fields.String()
    background = fields.String()
    name = fields.String()

class GetHeroBlockSchema(Schema):
    type = fields.Enum(HeroBlockType, by_value=True)
    data = fields.Raw()

    @pre_dump
    def f(self, obj, *args, many=False, **kwargs):
        if obj.type == HeroBlockType.MANGA:
            obj.data = GetHeroBlockManga().dump(obj.data, *args, **kwargs)
        else:
            raise ValueError('Invalid hero block type')
        
        return obj


class GetReadingProgressSchema(Schema):
    id = fields.Integer()
    page = fields.Integer()
    manga = fields.Nested("GetMangaSchemaMini")
    chapter = fields.Nested("GetChapterSchemaMini")

class GetHomeMapItemSchema(Schema):
    type = fields.Enum(HomeBlockType, by_value=True)
    title = fields.String()
    hash = fields.String()

class GetHomeBlocksListSchema(Schema):
    blocks_hash = fields.List(fields.String())

class GetLastAddedChaptersPaginationSchema(Schema):
    cursor = fields.Dict()
    has_more = fields.Boolean()

class GetLastAddedChaptersSchema(Schema):
    chapters = fields.List(fields.Nested("GetChapterSchemaMini"))
    pagination = fields.Nested("GetLastAddedChaptersPaginationSchema")

class GetHomeBlockSchema(Schema):
    # Маппинг: HomeBlockType -> Класс схемы marshmallow
    TYPE_MAPPING = {
        HomeBlockType.HERO: GetHeroBlockSchema,
        HomeBlockType.READING_PROGRESSES: GetReadingProgressSchema,
        HomeBlockType.MANGA_LIST: GetMangaSchemaMini,
        HomeBlockType.LAST_ADDED_CHAPTERS: GetLastAddedChaptersSchema,
    }

    def _serialize_block(self, block_type, block_data):
        schema_cls = self.TYPE_MAPPING.get(block_type)
        if not schema_cls:
            raise ValueError(
                f'Unsupported block type: {block_type}. '
                f'Make sure it is registered in TYPE_MAPPING.'
            )

        is_collection = isinstance(block_data, Sequence) and not isinstance(
            block_data, (str, bytes, dict)
        )

        return schema_cls().dump(block_data, many=is_collection)

    def _serialize(self, obj, *, many=False, **kwargs):
        if obj is None:
            return None

        if many:
            return [self._serialize_block(block_type, block_data) for block_type, block_data in obj]
        else:
            block_type, data = obj

            if not obj:
                return None
            
            return self._serialize_block(block_type, data)
        

        
