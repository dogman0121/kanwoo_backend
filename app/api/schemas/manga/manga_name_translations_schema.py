from marshmallow import Schema, fields


class MangaNameTranslationsSchema(Schema):
    lang = fields.String(required=True)
    name = fields.String(required=True)
