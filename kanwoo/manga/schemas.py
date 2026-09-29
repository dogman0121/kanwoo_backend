from marshmallow import Schema, fields, pre_dump

from kanwoo.schemas import File, Json
from kanwoo.schemas import LanguageSchema, PrivacySchema
from kanwoo.profile.schemas import ProfileSchema
from kanwoo.entity import FileAction

MANGA_POSTER_MAX_SIZE = 4 * 1024 * 1024
MANGA_POSTER_ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.webp']
MANGA_POSTER_ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

MANGA_BACKGROUND_MAX_SIZE = 10 * 1024 * 1024
MANGA_BACKGROUND_ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.webp']
MANGA_BACKGROUND_ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

MANGA_PROMO_LOGO_MAX_SIZE = 10 * 1024 * 1024
MANGA_PROMO_LOGO_ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.webp']
MANGA_PROMO_LOGO_ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

MANGA_PROMO_NAME_MAX_SIZE = 10 * 1024 * 1024
MANGA_PROMO_NAME_ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.webp']
MANGA_PROMO_NAME_ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

MANGA_PROMO_BACKGROUND_MAX_SIZE = 10 * 1024 * 1024
MANGA_PROMO_BACKGROUND_ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.webp']
MANGA_PROMO_BACKGROUND_ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

class GetMangaTypeSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class GetMangaStatusSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class GetMangaAdultSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class GetMangaGenreSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class GetMangaPermissionSchema(Schema):
    edit = fields.Boolean()
    delete = fields.Boolean()
    verify = fields.Boolean()

class GetMangaNameTranslationsSchema(Schema):
    lang = fields.Nested(LanguageSchema)
    name = fields.String()

class GetMangaCreateNameTranslationSchema(Schema):
    lang = fields.Integer(required=True)
    name = fields.String(required=True)

class GetMangaTranslationSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)
    lang = fields.Nested(LanguageSchema)
    privacy = fields.Nested(PrivacySchema)
    is_official = fields.Boolean()

class GetMangaPosterSchema(Schema):
    thumbnail = fields.String()
    small = fields.String()
    medium = fields.String()
    large = fields.String()
    orig = fields.String()

class GetMangaTranslationSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)

class GetMangaTranslationCreateSchema(Schema):
    name = fields.String()
    privacy = fields.Integer()
    is_official = fields.Boolean()

class GetMangaPermissionSchema(Schema):
    edit = fields.Boolean()
    view = fields.Boolean()

class GetMangaStatsSchema(Schema):
    views = fields.Integer()
    saves = fields.Integer()

class GetMangaSchemaMini(Schema):
    id = fields.Integer(required=True)
    slug = fields.String(required=True)
    name = fields.String(required=True)
    poster = fields.Nested(GetMangaPosterSchema)
    status = fields.Nested(GetMangaStatusSchema)
    type = fields.Nested(GetMangaTypeSchema)
    adult = fields.Nested(GetMangaAdultSchema)
    year = fields.Integer()

class GetMangaSchemaFull(GetMangaSchemaMini):
    name_translations = fields.List(fields.Nested(GetMangaNameTranslationsSchema))
    description = fields.String()
    genres = fields.List(fields.Nested(GetMangaGenreSchema))
    stats = fields.Nested(GetMangaStatsSchema)
    background = fields.String()
    promo_name = fields.String()
    promo_logo = fields.String()
    promo_background = fields.String()
    creator = fields.Nested(ProfileSchema)
    author = fields.Nested(ProfileSchema)
    created_at = fields.DateTime()

    @pre_dump
    def get_stats(self, obj, many):
        obj.stats = {
            "views": obj.views,
            "saves": obj.saves
        }

        return obj
    
class MangaCreateSchema(Schema):
    name = fields.String()
    name_translations = Json()
    description = fields.String(allow_none=True)
    status = fields.Integer()
    type = fields.Integer()
    adult = fields.Integer()
    genres = fields.List(fields.Integer())
    year = fields.Integer()
    privacy = fields.Integer()
    background = File(
        max_file_size=MANGA_BACKGROUND_MAX_SIZE, 
        allowed_file_types=MANGA_BACKGROUND_ALLOWED_TYPES, 
        allowed_file_ext=MANGA_BACKGROUND_ALLOWED_EXTENSIONS,
        allow_none=True
    )
    poster = File(
        max_file_size=MANGA_POSTER_MAX_SIZE, 
        allowed_file_types=MANGA_POSTER_ALLOWED_TYPES, 
        allowed_file_ext=MANGA_POSTER_ALLOWED_EXTENSIONS
    )


class MangaUpdateSchema(Schema):
    slug = fields.String()
    name = fields.String()
    name_translations = Json()
    description = fields.String(allow_none=True)
    status = fields.Integer()
    type = fields.Integer()
    adult = fields.Integer()
    genres = fields.List(fields.Integer())
    year = fields.Integer()
    privacy = fields.Integer()
    background = File(
        max_file_size=MANGA_BACKGROUND_MAX_SIZE, 
        allowed_file_types=MANGA_BACKGROUND_ALLOWED_TYPES, 
        allowed_file_ext=MANGA_BACKGROUND_ALLOWED_EXTENSIONS,
        allow_none=True
    )
    poster = File(
        max_file_size=MANGA_POSTER_MAX_SIZE, 
        allowed_file_types=MANGA_POSTER_ALLOWED_TYPES, 
        allowed_file_ext=MANGA_POSTER_ALLOWED_EXTENSIONS,
        allow_none=True
    )
    promo_name = File(
        max_file_size=MANGA_PROMO_NAME_MAX_SIZE, 
        allowed_file_types=MANGA_PROMO_NAME_ALLOWED_TYPES, 
        allowed_file_ext=MANGA_PROMO_NAME_ALLOWED_EXTENSIONS,
        allow_none=True
    )
    promo_logo = File(
        max_file_size=MANGA_PROMO_LOGO_MAX_SIZE, 
        allowed_file_types=MANGA_PROMO_LOGO_ALLOWED_TYPES, 
        allowed_file_ext=MANGA_PROMO_LOGO_ALLOWED_EXTENSIONS,
        allow_none=True
    )
    promo_background = File(
        max_file_size=MANGA_PROMO_BACKGROUND_MAX_SIZE, 
        allowed_file_types=MANGA_PROMO_BACKGROUND_ALLOWED_TYPES, 
        allowed_file_ext=MANGA_PROMO_BACKGROUND_ALLOWED_EXTENSIONS,
        allow_none=True
    )
    background_action = fields.Enum(FileAction, by_value=True)
    poster_action = fields.Enum(FileAction, by_value=True)
    promo_name_action = fields.Enum(FileAction, by_value=True)
    promo_logo_action = fields.Enum(FileAction, by_value=True)
    promo_background_action = fields.Enum(FileAction, by_value=True)

    
class MangaChapterSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    tome = fields.Integer()
    chapter = fields.Integer()
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)
    privacy = fields.Nested(PrivacySchema)


class ReadingProgressUpdateSchema(Schema):
    chapter = fields.Integer()
    page = fields.Integer()


class ReadingProgressSchema(Schema):
    manga = fields.Nested(GetMangaSchemaFull)
    chapter = fields.Nested("ChapterSchemaMini")

class MangaEditFormDataSchema(GetMangaSchemaFull):
    privacy = fields.Nested(PrivacySchema)


class MangaSuggestionCreateSchema(Schema):
    link = fields.String()
    name = fields.String()
    comment = fields.String()

class MangaSuggestionSchema(Schema):
    id = fields.Integer()
    link = fields.String()
    name = fields.String()
    comment = fields.String()
    created_at = fields.DateTime()
    creator = fields.Nested("ProfileSchema")

class MangaTranslationCreateSchema(Schema):
    name = fields.String()
    privacy = fields.Integer()
    is_official = fields.Boolean()