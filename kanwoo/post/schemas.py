from marshmallow import fields, Schema
from marshmallow.validate import Length

class PostSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    creator = fields.Nested("ProfileSchema")
    created_at = fields.DateTime()

class PostCreateSchema(Schema):
    text = fields.String(validate=[Length(max=1000)])