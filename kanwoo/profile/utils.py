from datetime import datetime, timedelta
from flask import current_app

def set_auth_profile_cookie(response, profile):
    response.set_cookie(
        "auth_profile", 
        str(profile.id), 
        expires=datetime.now() + timedelta(days=365),
        path="/",
        domain=current_app.config.get("DOMAIN"),
        secure=True,
        httponly=True,
    )