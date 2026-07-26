from marshmallow import Schema, fields, ValidationError, validate
import re

def validate_login(login):
    if re.fullmatch(r"^[a-z0-9_]+$", login) is None:
        raise ValidationError("Invalid login")

def validate_password(password):
    pass

class AuthRegisterSchema(Schema):
    code = fields.Integer(required=True)
    login = fields.String(required=True, validate=validate.And(validate.Length(max=32), validate_login))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=64))

class AuthLoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

class AuthEmailVerificationCodeSchema(Schema):
    email = fields.Email(required=True)

class AuthForgotSchema(Schema):
    email = fields.Email(required=True)

class AuthRecoverySchema(Schema):
    token = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate_password)


class AuthYandexOauthSchema(Schema):
    access_token = fields.String()
    expires_in = fields.String()
    extra_data = fields.Raw()
    token_type = fields.String()

class AuthChangePasswordSchema(Schema):
    old_password = fields.String()
    new_password = fields.String()