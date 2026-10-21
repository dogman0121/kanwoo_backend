from marshmallow import fields, Schema

from kanwoo.schemas import Json, File
from kanwoo.entity import FileAction
from kanwoo.manga.schemas import (
    GetMangaSchemaFull,
    MANGA_POSTER_ALLOWED_EXTENSIONS,
    MANGA_POSTER_ALLOWED_TYPES,
    MANGA_POSTER_MAX_SIZE,
    MANGA_BACKGROUND_ALLOWED_EXTENSIONS,
    MANGA_BACKGROUND_ALLOWED_TYPES,
    MANGA_BACKGROUND_MAX_SIZE,
    MANGA_PROMO_BACKGROUND_ALLOWED_EXTENSIONS,
    MANGA_PROMO_BACKGROUND_ALLOWED_TYPES,
    MANGA_PROMO_BACKGROUND_MAX_SIZE,
    MANGA_PROMO_LOGO_ALLOWED_EXTENSIONS,
    MANGA_PROMO_LOGO_ALLOWED_TYPES,
    MANGA_PROMO_LOGO_MAX_SIZE,
    MANGA_PROMO_NAME_ALLOWED_EXTENSIONS,
    MANGA_PROMO_NAME_ALLOWED_TYPES,
    MANGA_PROMO_NAME_MAX_SIZE
)
from kanwoo.translation.schemas import GetTranslationSchemaFull
from kanwoo.moderation.schemas import ModerationStatusTypeSchema
from kanwoo.chapter.schemas import GetChapterSchemaFull
from kanwoo.profile.schemas import (
    AvatarAction,
    PROFILE_AVATAR_ALLOWED_EXTENSIONS,
    PROFILE_AVATAR_ALLOWED_TYPES,
    PROFILE_AVATAR_MAX_SIZE,
    GetProfileSchema,
    GetProfilePermissionsSchema
)

class GetModerationStatusSchema(Schema):
    id = fields.Integer()
    status_type = fields.Nested(ModerationStatusTypeSchema)
    message = fields.String()
    created_at = fields.String()
    
class GetStudioMangaSchema(GetMangaSchemaFull):
    moderation_status = fields.Nested(GetModerationStatusSchema)

class GetStudioMangaInfoFormSchema(Schema):
    slug = fields.String(required=True)
    name = fields.String(required=True)
    poster = fields.Nested("GetMangaPosterSchema")
    status = fields.Nested("GetMangaStatusSchema")
    type = fields.Nested("GetMangaTypeSchema")
    adult = fields.Nested("GetMangaAdultSchema")
    year = fields.Integer()
    name_translations = fields.List(fields.Nested("GetMangaNameTranslationsSchema"))
    description = fields.String()
    genres = fields.List(fields.Nested("GetMangaGenreSchema"))
    background = fields.String()
    promo_name = fields.String()
    promo_logo = fields.String()
    promo_background = fields.String()
    author = fields.Nested("GetProfileSchema")
    privacy = fields.Nested("PrivacySchema")

    blocked_fields = fields.Method("get_blocked_fields")

    def get_blocked_fields(self, obj):
        return self.context.get("blocked_fields", [])


class GetStudioTranslationSchema(GetTranslationSchemaFull):
    name = fields.String()

class UpdateStudioTranslationSchema(Schema):
    name = fields.String()
    privacy_id = fields.Integer()

class CreateStudioProfileTranslationSchema(Schema):
    manga_id = fields.Integer()
    lang_id = fields.Integer()
    name = fields.String()
    privacy_id = fields.Integer()

class CreateStudioMangaTranslationSchema(Schema):
    lang_id = fields.Integer()
    name = fields.String()
    privacy_id = fields.Integer()

class GetStudioChapterSchema(GetChapterSchemaFull):
    pass

class CreateStudioChapterSchema(Schema):
    name = fields.String(allow_none=True)
    chapter = fields.Integer()
    privacy_id = fields.Integer()
    pages = fields.List(File())
    pages_order = Json(fields.List(fields.String()))
    extra_number = fields.Integer(allow_none=True)

class UpdateStudioChapterSchema(Schema):
    name = fields.String()
    chapter = fields.Integer()
    privacy_id = fields.Integer()
    extra_number = fields.Integer(allow_none=True)
    pages = fields.List(File())
    pages_order = Json(fields.List(fields.String()))

class CreateUpdateNameTranslationSchema(Schema):
    lang = fields.String()
    name = fields.String()

class CreateStudioMangaSchema(Schema):
    name = fields.String()
    name_translations = Json(fields.Nested(CreateUpdateNameTranslationSchema), allow_none=True)
    description = fields.String(allow_none=True)
    status_id = fields.Integer()
    type_id = fields.Integer()
    adult_id = fields.Integer()
    genres_ids = fields.List(fields.Integer())
    year = fields.Integer()
    privacy_id = fields.Integer()
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

class UpdateStudioMangaSchema(Schema):
    slug = fields.String()
    name = fields.String()
    name_translations = Json(fields.Nested(CreateUpdateNameTranslationSchema))
    description = fields.String(allow_none=True)
    status_id = fields.Integer()
    type_id = fields.Integer()
    adult_id = fields.Integer()
    genres_ids = fields.List(fields.Integer())
    year = fields.Integer()
    privacy_id = fields.Integer()
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

class CreateUpdateProfileLinkSchema(Schema):
    name = fields.String()
    link = fields.String()

class UpdateStudioProfileSchema(Schema):
    name = fields.String(required=True)
    slug = fields.String(required=True)
    about = fields.String()
    links = Json(fields.Nested(CreateUpdateProfileLinkSchema))
    avatar_action = fields.Enum(AvatarAction, by_value=True)
    avatar = File(
        max_file_size=PROFILE_AVATAR_MAX_SIZE, 
        allowed_file_types=PROFILE_AVATAR_ALLOWED_TYPES, 
        allowed_file_ext=PROFILE_AVATAR_ALLOWED_EXTENSIONS,
        allow_none=True
    )

class GetStudioProfileSchema(GetProfileSchema):
    pass

class GetStudioProfilePermissionSchema(GetProfilePermissionsSchema):
    pass