from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from app.jwt import jwt
from app.storage import Storage

migrate = Migrate()
db = SQLAlchemy()
mail = Mail()
cors = CORS(resources={r"/api/*": {"origins": "http://kanwoo.ru"}})
storage = Storage()
limiter = Limiter(
    get_remote_address,
    default_limits=["100 per minute"],
    headers_enabled=True,
    storage_uri="memory://",
    strategy="fixed-window"
)

from .create_app import create_app