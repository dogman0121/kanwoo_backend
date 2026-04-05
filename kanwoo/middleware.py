from datetime import datetime, timezone, timedelta
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    create_access_token,
    set_access_cookies
)
from flask_jwt_extended import get_jwt_identity



def setup_middleware(app):
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response