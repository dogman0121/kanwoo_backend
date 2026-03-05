from marshmallow import Schema, fields, pre_load, ValidationError, post_dump

from kanwoo.user.schemas import UserSchema
from kanwoo import storage
import json
import enum

class ProfileLinkSchema(Schema):
    name = fields.Str(required=True)
    link = fields.Str(required=True)

class ProfileCreateSchema(Schema):
    name = fields.String(required=True)
    about = fields.String()

class AvatarAction(enum.Enum):
    KEEP = "keep"
    REMOVE = "remove"
    UPDATE = "update"

class ProfileUpdateSchema(Schema):
    name = fields.String(required=True)
    slug = fields.String(required=True)
    about = fields.String()
    links = fields.List(fields.Nested(ProfileLinkSchema))
    avatar_action = fields.Enum(AvatarAction, by_value=True)

    @pre_load(pass_collection=False)
    def parse_link_json(self, data, many=True, **kwargs):
        if "links" not in data:
            return data
        
        links = data["links"]

        try:
            links_dict = json.loads(links)

            data["links"] = links_dict

            return data
        except json.JSONDecodeError:
            raise ValidationError("Invalid json", "links")


class ProfileSchema(Schema):
    id = fields.Integer(required=True)
    slug = fields.String()
    name = fields.String()
    about = fields.String()
    links = fields.Method(serialize="prepare_links")
    avatar = fields.String()
    creator = fields.Nested(UserSchema)
    created_at = fields.DateTime()

    def prepare_links(self, obj):
        links = []

        for i in obj.links:
            links.append({
                "name": i.name,
                "link": i.link
            })

        return links


class ProfilePermissionsSchema(Schema):
    edit = fields.Boolean()
    delete = fields.Boolean()


class ProfileReadingProgressSchema(Schema):
    chapter = fields.Nested("ChapterSchemaMini")
    manga = fields.Nested("MangaSchema")
    page = fields.Integer()
    updated_at = fields.DateTime()


class CurrentProfileSchema(ProfileSchema):
    role = fields.Integer()