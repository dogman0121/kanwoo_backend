import uuid

from app import db
from manage import app
from app.user.models import User
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    login = "SanSara"
    password = "g8SgEFPUhpiR"

    u = User(login=login, email=None, password=password)
    u.add()