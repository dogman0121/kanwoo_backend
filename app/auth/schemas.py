from marshmallow import Schema, fields, ValidationError
import re

def validate_login(login):
    if re.fullmatch(r"^[a-z0-9_]+$", login) is None:
        raise ValidationError("Invalid login")

class UserRegisterSchema(Schema):
    login = fields.Str(required=True, validate=validate_login)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
