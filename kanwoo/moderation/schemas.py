from marshmallow import Schema, fields

class ModerationStatusTypeSchema(Schema):
    id = fields.Integer()
    name = fields.String()

class ModerationStatus(Schema):
    id = fields.Integer()
    message = fields.String()
    created_at = fields.String()