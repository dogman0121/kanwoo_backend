import uuid

from app import db
from manage import app
from app.user.models import User
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    for user in User.query.all():
        user.is_verified = True

    db.session.commit()