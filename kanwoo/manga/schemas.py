from marshmallow import Schema, fields


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

class MangaTypeSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class MangaStatusSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class MangaAdultSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class MangaGenreSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class MangaPermissionSchema(Schema):
    edit = fields.Boolean()
    delete = fields.Boolean()
    verify = fields.Boolean()

class MangaNameTranslationsSchema(Schema):
    lang = fields.Nested(LanguageSchema)
    name = fields.String()

class MangaCreateNameTranslationSchema(Schema):
    lang = fields.Integer(required=True)
    name = fields.String(required=True)

class MangaTranslationSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)
    lang = fields.Nested(LanguageSchema)
    privacy = fields.Nested(PrivacySchema)
    is_official = fields.Boolean()

class MangaPosterSchema(Schema):
    thumbnail = fields.String()
    small = fields.String()
    medium = fields.String()
    large = fields.String()
    orig = fields.String()

class MangaTranslationSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)

class MangaTranslationCreateSchema(Schema):
    name = fields.String()
    privacy = fields.Integer()
    is_official = fields.Boolean()

class MangaPermissionSchema(Schema):
    edit = fields.Boolean()
    view = fields.Boolean()

class MangaSchema(Schema):
    id = fields.Integer(required=True)
    slug = fields.String(required=True)
    name = fields.String(required=True)
    name_translations = fields.List(fields.Nested(MangaNameTranslationsSchema))
    description = fields.String()
    status = fields.Nested(MangaStatusSchema)
    type = fields.Nested(MangaTypeSchema)
    adult = fields.Nested(MangaAdultSchema)
    genres = fields.List(fields.Nested(MangaGenreSchema))
    year = fields.Integer()
    views = fields.Integer()
    poster = fields.Nested(MangaPosterSchema)
    background = fields.String()
    promo_name = fields.String()
    promo_logo = fields.String()
    promo_background = fields.String()
    creator = fields.Nested(ProfileSchema)
    created_at = fields.DateTime()
    
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
    background_action = fields.Enum(FileAction, by_value=True)
    poster_action = fields.Enum(FileAction, by_value=True)
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
    manga = fields.Nested(MangaSchema)
    chapter = fields.Nested("ChapterSchemaMini")

class MangaEditFormDataSchema(MangaSchema):
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
    creator = fields.Nested("Profile")