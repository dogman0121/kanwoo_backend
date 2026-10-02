from marshmallow import Schema, fields

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
    id = fields.Integer()
    name = fields.String()
    preview = fields.List(fields.Nested("GetMangaPosterSchema"))
    description = fields.String()
    privacy = fields.Nested("PrivacySchema")
    creator = fields.Nested("ProfileSchema")
    created_at = fields.DateTime()
    manga_count = fields.Integer()