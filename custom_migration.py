import uuid

from app import db
from manage import app
from app.user.models import User
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    db.session.execute(text("""DROP TABLE IF EXISTS alembic_version;
DROP TYPE IF EXISTS list_visibility CASCADE;"""))

    db.session.commit()