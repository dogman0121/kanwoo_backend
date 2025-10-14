from marshmallow import Schema, fields

from app.manga.schemas import MangaSchema

class HomeSchema(Schema):
    hero = fields.List(fields.Nested(MangaSchema))
    newest = fields.List(fields.Nested(MangaSchema))
    ended = fields.List(fields.Nested(MangaSchema))
    random = fields.List(fields.Nested(MangaSchema))