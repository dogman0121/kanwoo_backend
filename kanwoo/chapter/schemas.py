import json

from app import storage
from app.entity import to_file
from app.profile.schemas import ProfileSchema
from app.translation.schemas import TranslationSchemaFull

from marshmallow import Schema, fields, pre_load, ValidationError

class PageSchema(Schema):
    uuid = fields.String()
    link = fields.Method("get_link")

    def get_link(self, obj):
        return storage.get_url(f"pages/{obj.uuid}{obj.ext}")  


class ChapterSchemaMini(Schema):
    id = fields.Integer()
    name = fields.String()
    tome = fields.Integer()
    chapter = fields.Integer()
    pages = fields.List(fields.Nested(PageSchema))
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)


class ChapterSchemaFull(ChapterSchemaMini):
    translation = fields.Nested(TranslationSchemaFull)

class ChapterCreateSchema(Schema):
    name = fields.String()
    tome = fields.Integer()
    chapter = fields.Integer()
    pages = fields.List(fields.Raw())
    pages_order = fields.List(fields.String())

    @pre_load
    def prepare_fields(self, data, **kwargs):
        try:
            data["pages_order"] = json.loads(data["pages_order"])
        except json.JSONDecodeError:
            raise ValidationError("Invalid json", "pages_order")

        data["pages"] = [to_file(i) for i in data["pages"]]

        return data