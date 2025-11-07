from app.profile.schemas import ProfileSchema
from app.manga.schemas import MangaSchema

from marshmallow import Schema, fields

class TranslationSchemaMini(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)

class TranslationSchemaFull(TranslationSchemaMini):
    manga = fields.Nested(MangaSchema)

class TranslationInfoFormSchema(Schema):
    translation = fields.Nested(TranslationSchemaMini)
    blocked_fields = fields.List(fields.String())