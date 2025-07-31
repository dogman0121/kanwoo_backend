import uuid

from app.infrastructure.databases import sqlalchemy_db as db
from manage import app
from sqlalchemy import text

with app.app_context():
    db.session.execute(text("DROP TABLE user CASCADE;"))

    db.session.commit()