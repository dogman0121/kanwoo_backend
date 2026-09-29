from marshmallow import Schema, fields, pre_dump

from .entities import HeroBlockType, HomeBlockType

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


class GetHomeReadingProgressSchema(Schema):
    id = fields.Integer()
    page = fields.Integer()
    manga = fields.Nested("GetMangaSchemaMini")
    chapter = fields.Nested("GetChapterSchemaMini")

class GetHomeMapItemSchema(Schema):
    type = fields.Enum(HomeBlockType, by_value=True)
    title = fields.String()
    hash = fields.String()
