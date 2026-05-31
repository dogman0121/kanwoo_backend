from flask import request
from functools import wraps

def pagination(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pagination = {}

        if 'page' in request.args:
            pagination['page'] = request.args.get('page', type=int)
        
        if 'per_page' in request.args:
            pagination['per_page'] = request.args.get('per_page', type=int)

        if 'last_id' in request.args:
            pagination['last_id'] = request.args.get('last_id', type=int)

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