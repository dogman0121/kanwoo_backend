from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from app.jwt import jwt
from app.storage import Storage

migrate = Migrate()
db = SQLAlchemy()
mail = Mail()
cors = CORS(resources={r"/api/*": {"origins": "https://kanwoo.ru"}})
storage = Storage()

from .create_app import create_app