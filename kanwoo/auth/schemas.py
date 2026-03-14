from marshmallow import Schema, fields, ValidationError
import re

def validate_login(login):
    if re.fullmatch(r"^[a-z0-9_]+$", login) is None:
        raise ValidationError("Invalid login")

def validate_password(password):
    pass

class AuthRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class AuthRecoverySchema(Schema):
    token = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate_password)
