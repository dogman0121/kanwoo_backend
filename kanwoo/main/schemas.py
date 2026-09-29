from marshmallow import Schema, fields

from kanwoo.schemas import LanguageSchema, PrivacySchema
from kanwoo.manga.schemas import GetMangaGenreSchema, GetMangaAdultSchema, GetMangaStatusSchema, GetMangaTypeSchema


class MetaMainSchema(Schema):
    languages = fields.List(fields.Nested(LanguageSchema))
    privacies = fields.List(fields.Nested(PrivacySchema))

class MangaMetaSchema(Schema):
    genres = fields.List(fields.Nested(GetMangaGenreSchema))
    statuses = fields.List(fields.Nested(GetMangaStatusSchema))
    types = fields.List(fields.Nested(GetMangaTypeSchema))
    adults = fields.List(fields.Nested(GetMangaAdultSchema))

class MetaSchema(Schema):
    main = fields.Nested(MetaMainSchema)
    manga = fields.Nested(MangaMetaSchema)
    
class FeedbackCreateSchema(Schema):
    message = fields.String()