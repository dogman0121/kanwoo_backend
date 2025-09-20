import uuid

from app import db
from manage import app
from app.user.models import User
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    res = db.session.execute(text("SELECT * FROM alembic_version;")).all()
    print(res)

    db.session.commit()