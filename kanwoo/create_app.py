from flask import Flask

from kanwoo.exceptions import setup_exceptions
from kanwoo.logs import setup_logs

from kanwoo import AppContainer
from kanwoo import (
    db, migrate, mail, cors, file_storage, limiter, cache, jwt
)
from kanwoo.jwt import setup_jwt_error_handlers
from kanwoo.routes import setup_routes
# from kanwoo.middleware import setup_middleware


def create_app(config):
    container = AppContainer()

    app = Flask(__name__)
    app.config.from_object(config)

    container.config.from_dict(app.config)
    app.container = container

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    file_storage.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    container.db_session.override(db.session)
    container.file_storage.override(file_storage)
    container.cache.override(cache)

    setup_routes(app)
    setup_exceptions(app)
    # setup_middleware(app)
    setup_logs(app)
    setup_jwt_error_handlers(jwt)

    return app