from typing import List

from marshmallow import Schema, fields, pre_dump
from marshmallow.experimental.context import Context

from kanwoo.schemas import LanguageSchema, PrivacySchema
from kanwoo.profile.schemas import GetProfileSchema

class GetTranslationSchemaMini(Schema):
    id = fields.Integer()
    owner = fields.Nested(GetProfileSchema)
    is_official = fields.Boolean()
    chapters_count = fields.Integer()

class GetTranslationSchemaFull(GetTranslationSchemaMini):
    created_at = fields.DateTime()
    creator = fields.Nested(GetProfileSchema)
    lang = fields.Nested(LanguageSchema)
    privacy = fields.Nested(PrivacySchema)

class GetTranslationInfoFormSchema(Schema):
    translation = fields.Nested(GetTranslationSchemaFull)
    blocked_fields = fields.List(fields.String())

class GetTranslationPermissionSchema(Schema):
    edit = fields.Boolean()

class GetTranslationViewerTranslationContextSchema(Schema):
    is_subscribed = fields.Boolean()

class GetTranslationViewerContextSchema(Schema):
    is_subscribed = fields.Boolean()

class GetTranslationContextSchema(Schema):
    viewer = fields.Nested(GetTranslationViewerContextSchema)
    manga = fields.Nested("GetMangaSchemaMini")
