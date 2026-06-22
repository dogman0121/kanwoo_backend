import pytest

from kanwoo import create_app, db, cache
from kanwoo.models import Privacy
from kanwoo.user.models import User
from kanwoo.profile.models import Profile

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
    with app.test_client() as client:
        yield client

@pytest.fixture()
def anonymous_client(client):
    return client

@pytest.fixture()
def jwt_service(container):
    return container.auth_container.jwt_service()

@pytest.fixture()
def access_token(app, user_id, jwt_service):
    with app.app_context():
        return jwt_service.create_access_token(user_id)
    
@pytest.fixture()
def refresh_token(app, user_id, jwt_service):
    with app.app_context():
        return jwt_service.create_refresh_token(user_id)
    
@pytest.fixture()
def csrf_access_token(app, jwt_service, access_token):
    with app.app_context():
        return jwt_service.get_csrf_token(access_token)

@pytest.fixture()
def csrf_refresh_token(app, jwt_service, refresh_token):
    with app.app_context():
        return jwt_service.get_csrf_token(refresh_token)

@pytest.fixture()
def authorized_client(app, client, profile_id, access_token, refresh_token, csrf_access_token, csrf_refresh_token):
    with app.app_context():

        client.set_cookie("access_token_cookie", access_token)
        client.set_cookie("csrf_access_token", csrf_access_token)
        client.set_cookie("refresh_token_cookie", refresh_token)
        client.set_cookie("csrf_refresh_token", csrf_refresh_token)
        client.set_cookie("auth_profile", str(profile_id))

    return client

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def user_id(app, container):
    hash_service = container.auth_container.hash_service()

    user = User(
        id=1,
        email="test@test.com",
        password=hash_service.generate_password_hash("12345678")
    )
    with app.app_context():
        db.session.add(user)

        db.session.commit()

        return user.id

@pytest.fixture()
def profile_id(app, user_id):
    profile = Profile(
        id=1,
        slug="test",
        name="test",
        about="test",
        owner_id=user_id,
        creator_id=user_id,
        role=1
    )

    with app.app_context():
        db.session.add(profile)

        db.session.commit()

        return profile.id


@pytest.fixture()
def privacy_id(app):
    privacy = Privacy(
        id=1,
        name="test"
    )

    with app.app_context():
        db.session.add(privacy)

        db.session.commit()

        return privacy.id