from marshmallow import Schema, fields

from kanwoo.list.models import ListVisibility
from kanwoo.user.schemas import UserSchema

class CreateListSchema(Schema):
    name = fields.String()
    description = fields.String(required=False, allow_none=True)
    visibility = fields.Enum(ListVisibility, by_value=True)

class ListSchema(Schema):
    id = fields.Int()
    name = fields.String()
    description = fields.String()
    visibility = fields.Enum(ListVisibility, by_value=True)
    creator = fields.Nested(UserSchema)
    created_at = fields.DateTime()