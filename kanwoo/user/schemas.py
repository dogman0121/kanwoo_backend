from marshmallow import Schema, fields


class UserSchema(Schema):
    login = fields.String()
    avatar = fields.String()

class UserMeSchema(Schema):
    id = fields.Integer()
    avatar = fields.String()
    email = fields.String()
    about = fields.String()
    subscribers_count = fields.Integer()
    role = fields.Integer()
    is_verified = fields.Boolean()
    created_at = fields.DateTime()