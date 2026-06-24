from marshmallow import Schema, fields, pre_dump


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

class HeroBlockSchema(Schema):
    type = fields.Enum(HeroBlockType, by_value=True)
    data = fields.Raw()

    @pre_dump
    def f(self, obj, *args, many=False, **kwargs):
        if obj.type == HeroBlockType.manga:
            obj.data = HeroBlockManga().dump(obj.data, *args, **kwargs)
        else:
            raise ValueError('Invalid animal type')
        
        return obj

