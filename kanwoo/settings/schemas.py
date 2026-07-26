from marshmallow import Schema, fields

class SettingsSecuritySchema(Schema):
    password_auth_enabled = fields.Boolean()
    yandex_oauth_enabled = fields.Boolean()


class SettingsNotificationSchema(Schema):
    pass