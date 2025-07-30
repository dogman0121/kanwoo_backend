from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

def get_access_token(user_id):
    return create_access_token(identity=user_id)

def get_refresh_token(user_id):
    return create_refresh_token(identity=user_id)