from marshmallow import Schema, fields

from kanwoo.entity import FileAction
from kanwoo.schemas import Json, File
from kanwoo.manga.schemas import (
    MANGA_BACKGROUND_ALLOWED_EXTENSIONS,
    MANGA_BACKGROUND_ALLOWED_TYPES,
    MANGA_BACKGROUND_MAX_SIZE,
    MANGA_POSTER_ALLOWED_EXTENSIONS,
    MANGA_POSTER_ALLOWED_TYPES,
    MANGA_POSTER_MAX_SIZE,
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
from kanwoo.moderation.schemas import ModerationStatusTypeSchema


class AdminMainDashboardSchema(Schema):
    manga_reports_count = fields.Integer()
    chapters_reports_count = fields.Integer()
    manga_waiting_moderation_count = fields.Integer()
    chapter_waiting_moderation_count = fields.Integer()
    manga_sugesstions_count = fields.Integer()
    feedback_messages_count = fields.Integer()

class AdminModerationStatusSchema(Schema):
    id = fields.Integer()
    status_type = fields.Nested(ModerationStatusTypeSchema)
    message = fields.String()
    created_at = fields.String()
    creator = fields.Nested("ProfileSchema")

class AdminChapterSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    chapter = fields.Integer()
    created_at = fields.DateTime()
    creator = fields.Nested("ProfileSchema")
    privacy = fields.Nested("PrivacySchema")

class AdminMangaCreateSchema(Schema):
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

class AdminMangaUpdateSchema(Schema):
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

class AdminMangaSchema(Schema):
    id = fields.Integer(required=True)
    slug = fields.String(required=True)
    name = fields.String(required=True)
    name_translations = fields.List(fields.Nested("MangaNameTranslationsSchema"))
    description = fields.String()
    status = fields.Nested("MangaStatusSchema")
    type = fields.Nested("MangaTypeSchema")
    adult = fields.Nested("MangaAdultSchema")
    genres = fields.List(fields.Nested("MangaGenreSchema"))
    privacy = fields.Nested("PrivacySchema")
    year = fields.Integer()
    views = fields.Integer()
    poster = fields.Nested("MangaPosterSchema")
    background = fields.String()
    promo_name = fields.String()
    promo_logo = fields.String()
    promo_background = fields.String()
    creator = fields.Nested("ProfileSchema")
    author = fields.Nested("ProfileSchema")
    created_at = fields.DateTime()
    moderation_status = fields.Nested(AdminModerationStatusSchema)
    moderation_history = fields.List(fields.Nested(AdminModerationStatusSchema))
    

class AdminAddModerationStatusSchema(Schema):
    status_type = fields.Integer()
    message = fields.String()


class AdminFeedbackSchema(Schema):
    id = fields.Integer()
    message = fields.String()
    created_at = fields.String()
    resolved_at = fields.String()
    creator = fields.Nested("ProfileSchema")
    resolver = fields.Nested("ProfileSchema")

class AdminMangaReportSchema(Schema):
    id = fields.Integer()
    message = fields.String()
    created_at = fields.String()
    resolved_at = fields.String()
    creator = fields.Nested("ProfileSchema")
    resolver = fields.Nested("ProfileSchema")
    manga = fields.Nested(AdminMangaSchema)

class AdminChapterReportSchema(Schema):
    id = fields.Integer()
    message = fields.String()
    created_at = fields.String()
    resolved_at = fields.String()
    creator = fields.Nested("ProfileSchema")
    resolver = fields.Nested("ProfileSchema")
    chapter = fields.Nested(AdminMangaSchema)

class AdminMangaSuggestionSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    comment = fields.String()
    link = fields.String()
    created_at = fields.DateTime()
    resolved_at = fields.DateTime()
    creator = fields.Nested("ProfileSchema")
    resolver = fields.Nested("ProfileSchema")