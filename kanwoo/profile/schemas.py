from marshmallow import Schema, fields, pre_load, ValidationError
from marshmallow.experimental.context import Context

from kanwoo.schemas import File, Json
from kanwoo.user.schemas import UserSchema
import json
import enum

PROFILE_AVATAR_MAX_SIZE = 4 * 1024 * 1024
PROFILE_AVATAR_ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.webp']
PROFILE_AVATAR_ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

class ProfileLinkSchema(Schema):
    name = fields.Str(required=True)
    link = fields.Str(required=True)

class ProfileCreateSchema(Schema):
    avatar = File(
        max_file_size=PROFILE_AVATAR_MAX_SIZE, 
        allowed_file_types=PROFILE_AVATAR_ALLOWED_TYPES, 
        allowed_file_ext=PROFILE_AVATAR_ALLOWED_EXTENSIONS,
        allow_none=True
    )
    name = fields.String(required=True)
    slug = fields.String(required=True)

class AvatarAction(enum.Enum):
    KEEP = "keep"
    REMOVE = "remove"
    UPDATE = "update"

class ProfileUpdateSchema(Schema):
    name = fields.String(required=True)
    slug = fields.String(required=True)
    about = fields.String()
    links = Json()
    avatar_action = fields.Enum(AvatarAction, by_value=True)
    avatar = File(
        max_file_size=PROFILE_AVATAR_MAX_SIZE, 
        allowed_file_types=PROFILE_AVATAR_ALLOWED_TYPES, 
        allowed_file_ext=PROFILE_AVATAR_ALLOWED_EXTENSIONS,
        allow_none=True
    )


class ProfileLinkSchema(Schema):
    name = fields.String()
    link = fields.String()

class ProfileSchema(Schema):
    id = fields.Integer(required=True)
    slug = fields.String()
    name = fields.String()
    about = fields.String()
    links = fields.List(fields.Nested(ProfileLinkSchema))
    avatar = fields.String()
    creator = fields.Nested(UserSchema)
    created_at = fields.DateTime()


class ProfilePermissionsSchema(Schema):
    edit = fields.Boolean()
    delete = fields.Boolean()


class ProfileReadingProgressSchema(Schema):
    chapter = fields.Nested("ChapterSchemaMini")
    manga = fields.Nested("MangaSchema")
    page = fields.Integer()
    updated_at = fields.DateTime()


class ProfileCollectionSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    privacy = fields.Nested("PrivacySchema")
    manga_count = fields.Integer()
    contain_manga = fields.Method("get_contain_manga")
    created_at = fields.DateTime()
    creator = fields.Nested("ProfileSchema")

    def get_contain_manga(self, obj):
        manga_slug = Context.get()['manga_slug']

        if manga_slug:
            return obj.contain_manga(manga_slug)
        
        return None

class CurrentProfileSchema(ProfileSchema):
    role = fields.Integer()