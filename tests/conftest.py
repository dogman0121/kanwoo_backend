import pytest

from kanwoo import create_app, db, cache

from . import TestConfig

@pytest.fixture
def app():
    test_config = TestConfig()

    app = create_app(test_config)
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    with app.app_context():
        db.create_all()

    yield app

    # clean up / reset resources here
    with app.app_context():
        db.drop_all()
        cache.flush()

@pytest.fixture()
def container(app):
    return app.container

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()