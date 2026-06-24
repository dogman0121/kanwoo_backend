from kanwoo.schemas import LanguageSchema, PrivacySchema
from kanwoo.profile.schemas import ProfileSchema

from marshmallow import Schema, fields

class TranslationCreateSchema(Schema):
    pass

class TranslationSchemaMini(Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)
    owner = fields.Nested(ProfileSchema)
    lang = fields.Nested(LanguageSchema)
    privacy = fields.Nested(PrivacySchema)
    is_official = fields.Boolean()
    chapters_count = fields.Integer()

class TranslationSchemaFull(Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)
    owner = fields.Nested(ProfileSchema)
    lang = fields.Nested(LanguageSchema)
    privacy = fields.Nested(PrivacySchema)
    is_official = fields.Boolean()
    manga = fields.Nested("MangaSchema")
    chapters_count = fields.Integer()

class TranslationInfoFormSchema(Schema):
    translation = fields.Nested(TranslationSchemaMini)
    blocked_fields = fields.List(fields.String())

class TranslationCreateSchema(Schema):
    manga = fields.Integer()
    name = fields.String()
    privacy = fields.Integer()
    is_official = fields.Boolean()

class TranslationUpdateSchema(Schema):
    name = fields.String()
    privacy = fields.Integer()

class TranslationPermissionSchema(Schema):
    edit = fields.Boolean()