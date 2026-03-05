from marshmallow import Schema, fields, pre_dump

from kanwoo import storage
from kanwoo.manga.schemas import MangaSchema

import enum

class HeroBlockType(enum.Enum):
    manga = "manga"

class HeroBlockData(Schema):
    pass

class HeroBlockManga(HeroBlockData):
    slug = fields.String()
    logo = fields.String()
    background = fields.String()
    name = fields.String()

class HeroBlock(Schema):
    type = fields.Enum(HeroBlockType, by_value=True)
    data = fields.Raw()

    @pre_dump
    def f(self, obj, *args, **kwargs):
        if obj.type == HeroBlockType.manga:
            obj.data = HeroBlockManga().dump(obj.data, *args, **kwargs)
        else:
            raise ValueError('Invalid animal type')
        
        return obj

class HomeSchema(Schema):
    hero = fields.List(fields.Nested(lambda: HeroBlock()))
    newest = fields.List(fields.Nested(MangaSchema))
    ended = fields.List(fields.Nested(MangaSchema))
    random = fields.List(fields.Nested(MangaSchema))
