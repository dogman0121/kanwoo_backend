from unittest.mock import create_autospec

from kanwoo import AppContainer
from kanwoo.email import EmailService
from kanwoo.user.services import UserService
from kanwoo.user.models import User
from kanwoo.auth.services import HashService, VerificationCodeService
from kanwoo.auth.dto import AuthRegisterDTO


def test_send_email_verification_code(app, container):
    email_param = "a@mail.com"

    mock_verification_code_service = create_autospec(VerificationCodeService)
    mock_email_service = create_autospec(EmailService)

    mock_verification_code_service.get_email_verification_code.return_value = 111111

    with (
        container.email_service.override(mock_email_service),
        container.auth_container.verification_code_service.override(mock_verification_code_service)
    ):
        auth_service = container.auth_container.auth_service()

        with app.app_context():
            auth_service.system_send_email_verification_message(email_param)

    mock_verification_code_service.get_email_verification_code.assert_called()
    mock_verification_code_service.get_email_verification_code.assert_called_with(email_param)
    mock_email_service.send_email.assert_called()

def test_register_user(app, container: AppContainer):
    code_param = 111111
    email_param = "a@mail.com"
    password_param="123456"

    register_dto = AuthRegisterDTO(
        code=code_param,
        email=email_param,
        password=password_param
    )

    mock_user_service = create_autospec(UserService)
    mock_hash_service = create_autospec(HashService)
    mock_verification_code_service = create_autospec(VerificationCodeService)

    mock_user_service.system_create_user.return_value = User(id=1, email=email_param, password=password_param)
    mock_hash_service.generate_password_hash.return_value = password_param
    mock_verification_code_service.check_email_verification_code.return_value = True

    with (
        container.auth_container.user_service.override(mock_user_service),
        container.auth_container.verification_code_service.override(mock_verification_code_service),
        container.auth_container.hash_service.override(mock_hash_service)
    ):
        auth_service = container.auth_container.auth_service()

        with app.app_context():
            registred_user = auth_service.system_register_user(register_dto)

    assert registred_user.email == email_param
    assert registred_user.password == password_param

    mock_verification_code_service.check_email_verification_code.assert_called_with(email_param, code_param)