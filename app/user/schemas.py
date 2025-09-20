from marshmallow import Schema, fields


class UserSchema(Schema):
    login = fields.String()
    avatar = fields.String()