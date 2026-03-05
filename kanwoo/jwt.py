from flask_jwt_extended import JWTManager
from kanwoo.utils import respond

jwt = JWTManager()

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return respond(error="token_expired", detail={"token": ["Token expired"]}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return respond(error="invalid_token", detail={"token": ["Invalid token"]}), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return respond(error="missing_token", detail={"token": ["Missing authorization token"]}), 401

