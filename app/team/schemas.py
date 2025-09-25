from marshmallow import Schema, fields

from app.user.schemas import UserSchema


class TeamLinkSchema(Schema):
    type = fields.Str(required=True)
    link = fields.Str(required=True)

class TeamCreateSchema(Schema):
    name = fields.String(required=True)
    about = fields.String()
    link = fields.List(fields.Nested(TeamLinkSchema))

class TeamSchema(Schema):
    slug = fields.String()
    name = fields.String()
    about = fields.String()
    links = fields.List(fields.Nested(TeamLinkSchema))
    poster = fields.String()
    creator = fields.Nested(UserSchema)
    created_at = fields.DateTime()