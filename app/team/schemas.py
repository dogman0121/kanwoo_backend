from marshmallow import Schema, fields, pre_load, ValidationError, post_dump

from app.user.schemas import UserSchema
from app import storage
import json
import enum

class TeamLinkSchema(Schema):
    name = fields.Str(required=True)
    link = fields.Str(required=True)

class TeamCreateSchema(Schema):
    name = fields.String(required=True)
    about = fields.String()

class AvatarAction(enum.Enum):
    KEEP = "keep"
    REMOVE = "remove"
    UPDATE = "update"

class TeamUpdateSchema(Schema):
    name = fields.String(required=True)
    slug = fields.String(required=True)
    about = fields.String()
    links = fields.List(fields.Nested(TeamLinkSchema))
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


class TeamSchema(Schema):
    slug = fields.String()
    name = fields.String()
    about = fields.String()
    links = fields.Method(serialize="prepare_links")
    avatar = fields.Method(serialize="prepare_avatar")
    creator = fields.Nested(UserSchema)
    created_at = fields.DateTime()

    def prepare_avatar(self, obj):
        if obj.avatar is None:
            return None
        
        avatar = storage.get_url(f"teams/{obj.id}/{obj.avatar.uuid}{obj.avatar.ext}")

        return avatar
    
    def prepare_links(self, obj):
        links = []

        for i in obj.links:
            links.append({
                "name": i.name,
                "link": i.link
            })

        return links