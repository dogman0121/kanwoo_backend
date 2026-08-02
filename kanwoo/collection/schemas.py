from marshmallow import Schema, fields

from kanwoo.user.schemas import UserSchema

class CollectionCreateSchema(Schema):
    name = fields.String()
    privacy = fields.Integer()

class CollectionUpdateSchema(Schema):
    name = fields.String()
    description = fields.String()
    privacy = fields.Integer()

class CollectionAddMangaSchema(Schema):
    manga = fields.String()

class CollectionRemoveMangaSchema(Schema):
    manga = fields.String()
    
class CollectionSchema(Schema):
    id = fields.Int()
    name = fields.String()
    description = fields.String()
    privacy = fields.Nested("PrivacySchema")
    creator = fields.Nested("ProfileSchema")
    manga = fields.List(fields.Nested("MangaSchema"))
    created_at = fields.DateTime()