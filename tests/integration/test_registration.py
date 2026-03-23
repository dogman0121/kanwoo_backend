from unittest.mock import create_autospec

from kanwoo import cache
from kanwoo.email import EmailService
from kanwoo.auth.dto import AuthRegisterDTO

def test_get_email_verification_code(app, container):
    email_param = "a@email.com"

    mock_email_service = create_autospec(EmailService)

    with container.email_service.override(mock_email_service):
        auth_service = container.auth_container.auth_service()

        with app.app_context():
            auth_service.system_send_email_verification_message(email_param)

    mock_email_service.send_email.assert_called()
    assert cache.get(f"auth:verification:code:{email_param}") != None

def test_registration(app, container):
    pass