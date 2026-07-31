from marshmallow import Schema, fields

class ReadingProgressSchema(Schema):
    id = fields.Integer()
    manga = fields.Nested("MangaSchema")
    chapter = fields.Nested("ChapterSchemaMini")
    chapters_count = fields.Integer()
    created_at = fields.DateTime()