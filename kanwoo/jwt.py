from flask_jwt_extended import JWTManager
from kanwoo.utils import respond

def expired_token_callback(jwt_header, jwt_payload):
    return respond(error="token_expired", detail={"token": ["Token expired"]}), 401

def invalid_token_callback(error):
    return respond(error="invalid_token", detail={"token": ["Invalid token"]}), 401


def unauthorized_callback(error):
    return respond(error="missing_token", detail={"token": ["Missing authorization token"]}), 401

def setup_jwt_error_handlers(jwt: JWTManager):
    jwt.expired_token_loader(expired_token_callback)
    jwt.invalid_token_loader(invalid_token_callback)
    jwt.unauthorized_loader(unauthorized_callback)



