from marshmallow import fields, Schema

from .entity import NotificationDeleteModeEnum

class NotificationSchema(Schema):
    id = fields.Integer()


class NotificationDeleteSchema(Schema):
    mode = fields.Enum(NotificationDeleteModeEnum, by_value=True)
    notifications = fields.List(fields.Integer(), allow_none=True)