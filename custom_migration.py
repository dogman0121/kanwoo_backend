import uuid

from app import db
from manage import app
from app.team.models import TeamLink
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    print(db.session.execute(text("SELECT * FROM information_schema.rows WHERE table_name = 'team_link';")).all())

    #db.session.commit()