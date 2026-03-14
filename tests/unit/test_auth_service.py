from unittest.mock import Mock, create_autospec
from dependency_injector import providers

from kanwoo import AppContainer
from kanwoo.email import EmailService
from kanwoo.user.services import UserService
from kanwoo.user.models import User
from kanwoo.auth.services import HashService

def test_register_user(app, container: AppContainer):
    email_param = "a@mail.com"
    password_param = "123456"

    mock_user_service = create_autospec(UserService)
    mock_email_service = create_autospec(EmailService)
    mock_hash_service = create_autospec(HashService)

    mock_user_service.system_create_user.return_value = User(id=1, email=email_param, password=password_param)
    mock_hash_service.generate_password_hash.return_value = password_param

    with (
        container.auth_container.user_service.override(mock_user_service),
        container.email_service.override(mock_email_service),
        container.auth_container.hash_service.override(mock_hash_service)
    ):
        auth_service = container.auth_container.auth_service()

        with app.app_context():
            registred_user = auth_service.system_register_user(email_param, password_param)

    assert registred_user.email == email_param
    assert registred_user.password == password_param
    mock_email_service.send_email.assert_called()