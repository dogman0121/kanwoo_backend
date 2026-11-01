import json

from kanwoo.schemas import PrivacySchema, RefAttrSchema
from kanwoo.profile.schemas import GetProfileSchema

from marshmallow import Schema, fields

class GetPageSchema(Schema):
    uuid = fields.String()
    link = fields.Method("get_link")
    orig_filename = fields.String()
    width = fields.Integer()
    height = fields.Integer()

    def get_link(self, obj):
        return str(obj)


class GetChapterSchemaMini(Schema):
    id = fields.Integer()
    name = fields.String()
    chapter = fields.Integer()
    pages_count = fields.Integer()

class GetChapterSchemaFull(GetChapterSchemaMini):
    privacy = fields.Nested(PrivacySchema)
    next_chapter_id = fields.Integer()
    prev_chapter_id = fields.Integer()
    pages = fields.List(fields.Nested(GetPageSchema))
    creator = fields.Nested(GetProfileSchema)
    created_at = fields.DateTime()

class GetChapterContextSchema(Schema):
    translation = fields.Nested("GetTranslationSchemaFull")
    manga = fields.Nested("GetMangaSchemaMini")
    
class ChapterPermissionsSchema(Schema):
    edit = fields.Boolean()
    
class ChapterReadingProgressSchema(Schema):
    page = fields.Integer()


class ChapterUpdateReadingProgressSchema(Schema):
    page = fields.Integer()

class PageMetadataSchema(Schema):
    width = fields.Integer()
    height = fields.Integer()

class ChapterMetadataSchema(Schema):
    pages = fields.List(fields.Nested(PageMetadataSchema))