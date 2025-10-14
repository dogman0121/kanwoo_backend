import uuid

from app import db
from app.profiles.models import Profile
from app.user.models import User
from manage import app
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    for u in User.query.all():
        p = Profile(
            slug=u.login,
            name=u.login,
            creator_id=u.id
        )
        p.add()

    # db.session.execute(text("DELETE FROM notification;"))

    db.session.commit()