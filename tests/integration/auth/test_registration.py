from unittest.mock import create_autospec
import pytest
import random

from kanwoo import cache
from kanwoo.email import EmailService
from kanwoo.auth.services import VerificationCodeService

def test_get_email_verification_code(app, container):
    email_param = "a@email.com"

    mock_email_service = create_autospec(EmailService)

    with container.email_service.override(mock_email_service):
        auth_service = container.auth_container.auth_service()

        with app.app_context():
            auth_service.system_send_email_verification_message(email_param)

    mock_email_service.send_email.assert_called()
    assert cache.get(f"auth:verification:code:{email_param}") != None


@pytest.mark.parametrize("run", range(5))
def test_register_with_long_login(container, client, faker, run):
    code = random.randint(100000, 999999)
    login = "a" * random.randint(65, 1000)
    email = faker.email()
    password = faker.password()

    mock_email_service = create_autospec(EmailService)
    mock_verification_code_service = create_autospec(VerificationCodeService)

    mock_verification_code_service.check_email_verification_code.return_value = True
    with (
        container.email_service.override(mock_email_service),
        container.auth_container.verification_code_service.override(mock_verification_code_service)
    ):
        response = client.post(
            "/v1/auth/register",
            json={
                "code": code,
                "login": login,
                "email": email,
                "password": password
            }
        )

        assert response.status_code == 400


@pytest.mark.parametrize("run", range(5))
def test_register_with_empty_login(container, client, faker, run):
    code = random.randint(100000, 999999)
    login = ""
    email = faker.email()
    password = faker.password()

    mock_email_service = create_autospec(EmailService)
    mock_verification_code_service = create_autospec(VerificationCodeService)

    mock_verification_code_service.check_email_verification_code.return_value = True
    with (
        container.email_service.override(mock_email_service),
        container.auth_container.verification_code_service.override(mock_verification_code_service)
    ):
        response = client.post(
            "/v1/auth/register",
            json={
                "code": code,
                "login": login,
                "email": email,
                "password": password
            }
        )

        assert response.status_code == 400


@pytest.mark.parametrize("run", range(5))
def test_register_with_empty_email(container, client, faker, run):
    code = random.randint(100000, 999999)
    login = faker.user_name()
    email = ""
    password = faker.password()

    mock_email_service = create_autospec(EmailService)
    mock_verification_code_service = create_autospec(VerificationCodeService)

    mock_verification_code_service.check_email_verification_code.return_value = True
    with (
        container.email_service.override(mock_email_service),
        container.auth_container.verification_code_service.override(mock_verification_code_service)
    ):
        response = client.post(
            "/v1/auth/register",
            json={
                "code": code,
                "login": login,
                "email": email,
                "password": password
            }
        )

        assert response.status_code == 400

@pytest.mark.parametrize("run", range(5))
def test_register_with_empty_password(container, client, faker, run):
    code = random.randint(100000, 999999)
    login = faker.user_name()
    email = faker.email()
    password = ""

    mock_email_service = create_autospec(EmailService)
    mock_verification_code_service = create_autospec(VerificationCodeService)

    mock_verification_code_service.check_email_verification_code.return_value = True
    with (
        container.email_service.override(mock_email_service),
        container.auth_container.verification_code_service.override(mock_verification_code_service)
    ):
        response = client.post(
            "/v1/auth/register",
            json={
                "code": code,
                "login": login,
                "email": email,
                "password": password
            }
        )

        assert response.status_code == 400

@pytest.mark.parametrize("run", range(5))
def test_register_with_existed_email(container, client, user, faker, run):
    code = random.randint(100000, 999999)
    login = faker.user_name()
    email = user.email,
    password = ""

    mock_email_service = create_autospec(EmailService)
    mock_verification_code_service = create_autospec(VerificationCodeService)

    mock_verification_code_service.check_email_verification_code.return_value = True
    with (
        container.email_service.override(mock_email_service),
        container.auth_container.verification_code_service.override(mock_verification_code_service)
    ):
        response = client.post(
            "/v1/auth/register",
            json={
                "code": code,
                "login": login,
                "email": email,
                "password": password
            }
        )

        assert response.status_code == 400

@pytest.mark.parametrize("run", range(5))
def test_register_with_existed_login(container, client, user, faker, run):
    code = random.randint(100000, 999999)
    login = faker.user_name()
    email = user.email
    password = faker.password()

    mock_email_service = create_autospec(EmailService)
    mock_verification_code_service = create_autospec(VerificationCodeService)

    mock_verification_code_service.check_email_verification_code.return_value = True
    with (
        container.email_service.override(mock_email_service),
        container.auth_container.verification_code_service.override(mock_verification_code_service)
    ):
        response = client.post(
            "/v1/auth/register",
            json={
                "code": code,
                "login": login,
                "email": email,
                "password": password
            }
        )

        assert response.status_code == 400