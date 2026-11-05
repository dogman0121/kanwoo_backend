from marshmallow import Schema, fields

class CreateCollectionSchema(Schema):
    name = fields.String()
    privacy = fields.Integer()

class UpdateCollectionSchema(Schema):
    name = fields.String()
    description = fields.String()
    privacy = fields.Integer()

class AddMangaIntoCollectionSchema(Schema):
    manga_id = fields.Integer()

class RemoveMangaFromCollectionSchema(Schema):
    manga_id = fields.Integer()

class GetCollectionViewerContextSchema(Schema):
    is_saved = fields.Boolean()

class GetCollectionContextSchema(Schema):
    viewer = fields.Nested(GetCollectionViewerContextSchema, allow_none=True)

class GetCollectionSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    preview = fields.List(fields.Nested("GetMangaPosterSchema"))
    description = fields.String()
    privacy = fields.Nested("PrivacySchema")
    creator = fields.Nested("GetProfileSchema")
    created_at = fields.DateTime()
    manga_count = fields.Integer()