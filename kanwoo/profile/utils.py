from datetime import datetime, timedelta
import os

def set_auth_profile_cookie(response, profile):
    response.set_cookie(
        "auth_profile", 
        str(profile.id), 
        expires=datetime.now() + timedelta(days=365),
        path="/",
        domain=os.getenv("SERVER_DOMAIN"),
        secure=True,
        httponly=True,
    )