import pytest
from kanwoo import create_app

from . import TestConfig

@pytest.fixture()
def app():
    app = create_app(TestConfig)
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def container(app):
    return app.container

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()