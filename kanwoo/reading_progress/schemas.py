from marshmallow import Schema, fields


class CreateReadingProgressSchema(Schema):
    chapter_id = fields.Integer()
    page = fields.Integer(allow_none=True)

class GetReadingProgressSchema(Schema):
    id = fields.Integer()
    page = fields.Integer()
    chapters_count = fields.Integer()
    created_at = fields.DateTime()

class GetReadingProgressContextSchema(Schema):
    chapter = fields.Nested("GetChapterSchemaMini", allow_none=True)
    manga = fields.Nested("GetMangaSchemaMini", allow_none=True)
    translation = fields.Nested("TranslationSchemaMini", allow_none=True)

class DeleteReadingProgressSchema(Schema):
    mode = fields.String()
    progresses_ids = fields.List(fields.Integer(), allow_none = True)

class UpdateReadingProgressSchema(Schema):
    page = fields.Integer()