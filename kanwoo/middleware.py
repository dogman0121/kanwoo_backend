from flask import request
from functools import wraps
import base64
import json

def decode_cursor(encoded_str: str):
    decoded_bytes = base64.b64decode(encoded_str)

    decoded_str = decoded_bytes.decode('utf-8')

    json_dict = json.loads(decoded_str)

    return json_dict

def pagination(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pagination = {}

        if 'page' in request.args:
            pagination['page'] = request.args.get('page', type=int)
        
        if 'per_page' in request.args:
            pagination['per_page'] = request.args.get('per_page', type=int)

        if 'cursor' in request.args:
            cursor_string = request.args.get('cursor')
            pagination['cursor'] = decode_cursor(cursor_string)

        if 'limit' in request.args:
            pagination['limit'] = request.args.get('limit', type=int)
        
        return func(*args, **pagination, **kwargs)
        
    return wrapper





# def setup_middleware(app):
#     @app.after_request
#     def refresh_expiring_jwts(response):
#         try:
#             exp_timestamp = get_jwt()["exp"]
#             now = datetime.now(timezone.utc)
#             target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#             if target_timestamp > exp_timestamp:
#                 access_token = create_access_token(identity=get_jwt_identity())
#                 set_access_cookies(response, access_token)
#             return response
#         except (RuntimeError, KeyError):
#             # Case where there is not a valid JWT. Just return the original response
#             return response