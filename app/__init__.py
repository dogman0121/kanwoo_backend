from flask import Flask

from app.api.auth import setup_jwt_manager
from app.api.controllers import setup_blueprints
from app.infrastructure.databases import setup_sqlalchemy
from app.infrastructure.storage import setup_file_storage
from app.jwt import jwt
from app.storage import Storage



def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    setup_blueprints(app)

    setup_sqlalchemy(app)

    setup_jwt_manager(app)

    setup_file_storage(app)

    return app