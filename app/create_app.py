from flask import Flask

from app.exceptions import setup_exceptions
from app.jwt import jwt

from app import (
    db, migrate, mail, cors, storage
)
from app.routes import setup_routes


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    storage.init_app(app)

    setup_routes(app)
    setup_exceptions(app)

    from app.admin import admin
    admin.init_app(app)

    return app