import json

from kanwoo.schemas import PrivacySchema
from kanwoo.entity import convert_to_file
from kanwoo.profile.schemas import ProfileSchema

from marshmallow import Schema, fields, pre_load, ValidationError

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
    creator = fields.Nested(ProfileSchema)
    created_at = fields.DateTime()

class GetChapterContextSchema(Schema):
    translation = fields.Nested("TranslationSchemaMini")
    manga = fields.Nested("GetMangaSchemaMini")

class ChapterCreateSchema(Schema):
    name = fields.String()
    chapter = fields.Integer()
    privacy = fields.Integer()
    pages = fields.List(fields.Raw())
    pages_order = fields.List(fields.String())

    @pre_load
    def prepare_fields(self, data, **kwargs):
        try:
            data["pages_order"] = json.loads(data["pages_order"])
        except json.JSONDecodeError:
            raise ValidationError("Invalid json", "pages_order")

        data["pages"] = [ convert_to_file(i) for i in data["pages"] ]

        return data
    
class ChapterPermissionsSchema(Schema):
    edit = fields.Boolean()

class ChapterUpdateSchema(Schema):
    name = fields.String()
    chapter = fields.Integer()
    privacy = fields.Integer()
    pages = fields.List(fields.Raw())
    pages_order = fields.List(fields.String())

    @pre_load
    def prepare_fields(self, data, **kwargs):
        try:
            data["pages_order"] = json.loads(data["pages_order"])
        except json.JSONDecodeError:
            raise ValidationError("Invalid json", "pages_order")

        data["pages"] = [ convert_to_file(i) for i in data["pages"] ]

        return data
    
class ChapterReadingProgressSchema(Schema):
    page = fields.Integer()


class ChapterUpdateReadingProgressSchema(Schema):
    page = fields.Integer()

class PageMetadataSchema(Schema):
    width = fields.Integer()
    height = fields.Integer()

class ChapterMetadataSchema(Schema):
    pages = fields.List(fields.Nested(PageMetadataSchema))