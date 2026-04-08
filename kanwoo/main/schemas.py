from marshmallow import Schema, fields

from kanwoo.schemas import LanguageSchema, PrivacySchema
from kanwoo.manga.schemas import MangaGenreSchema, MangaAdultSchema, MangaStatusSchema, MangaTypeSchema


class MetaMainSchema(Schema):
    languages = fields.List(fields.Nested(LanguageSchema))
    privacies = fields.List(fields.Nested(PrivacySchema))

class MangaMetaSchema(Schema):
    genres = fields.List(fields.Nested(MangaGenreSchema))
    statuses = fields.List(fields.Nested(MangaStatusSchema))
    types = fields.List(fields.Nested(MangaTypeSchema))
    adults = fields.List(fields.Nested(MangaAdultSchema))

class MetaSchema(Schema):
    main = fields.Nested(MetaMainSchema)
    manga = fields.Nested(MangaMetaSchema)
    
class FeedbackCreateSchema(Schema):
    message = fields.String()