from marshmallow import Schema, fields

from app.manga.schemas import MangaGenreSchema, MangaAdultSchema, MangaStatusSchema, MangaTypeSchema


class MetaSchema(Schema):
    genres = fields.List(fields.Nested(MangaGenreSchema))
    statuses = fields.List(fields.Nested(MangaStatusSchema))
    types = fields.List(fields.Nested(MangaTypeSchema))
    adults = fields.List(fields.Nested(MangaAdultSchema))