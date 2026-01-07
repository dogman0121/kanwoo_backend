from marshmallow import Schema, fields, pre_dump

from app import storage
from app.manga.schemas import MangaSchema

import enum

class HeroBlockType(enum.Enum):
    manga = "manga"

class HeroBlockData(Schema):
    pass

class HeroBlockManga(HeroBlockData):
    logo = fields.Method("get_logo")
    background = fields.Method("get_background")
    name = fields.Method("get_name")

    def get_logo(self, obj):
        return storage.get_url(f"manga/{obj.logo.uuid}{obj.logo.ext}")

    def get_background(self, obj):
        return storage.get_url(f"manga/{obj.background.uuid}{obj.background.ext}")

    def get_name(self, obj):
        return storage.get_url(f"manga/{obj.name.uuid}{obj.name.ext}")

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
