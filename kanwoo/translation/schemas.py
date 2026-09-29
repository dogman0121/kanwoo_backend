from typing import List

from marshmallow import Schema, fields, pre_dump
from marshmallow.experimental.context import Context

from kanwoo.schemas import LanguageSchema, PrivacySchema
from kanwoo.profile.schemas import ProfileSchema

class TranslationSchemaMini(Schema):
    id = fields.Integer()
    owner = fields.Nested(ProfileSchema)
    is_official = fields.Boolean()
    chapters_count = fields.Integer()

class TranslationSchema(TranslationSchemaMini):
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)
    lang = fields.Nested(LanguageSchema)
    privacy = fields.Nested(PrivacySchema)

class TranslationInfoFormSchema(Schema):
    translation = fields.Nested(TranslationSchema)
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

class TranslationViewerTranslationContextSchema(Schema):
    is_subscribed = fields.Boolean()

class TranslationViewerContextSchema(Schema):
    is_subscribed = fields.Boolean()


class TranslationContextSchema(Schema):
    viewer = fields.Nested(TranslationViewerContextSchema)

class TranslationListContextSchema(Schema):
    viewer = fields.Dict(keys=fields.Integer(), values=fields.Nested(TranslationViewerContextSchema))
