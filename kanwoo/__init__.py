from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from kanwoo.storage import Storage

migrate = Migrate()
db = SQLAlchemy(
    engine_options={
        "pool_pre_ping": True, 
        "pool_recycle": 300
    }
)
mail = Mail()
cors = CORS(
    origins=[
        "https://www.kanwoo.ru",
        "https://kanwoo.ru",
        "http://localhost:3000"  # для разработки
    ],
    supports_credentials=True,  # ← это включает Allow-Credentials
    allow_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
storage = Storage()
limiter = Limiter(
    get_remote_address,
    default_limits=["100 per minute"],
    headers_enabled=True,
    storage_uri="memory://",
    strategy="fixed-window"
)

from .containers import AppContainer

from .create_app import create_app