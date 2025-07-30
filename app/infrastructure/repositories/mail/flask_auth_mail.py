from flask_mail import Message
from flask import render_template

from app.domain.repositories.mail.auth_mail import AuthMail

from app.infrastructure.mail import mail

from threading import Thread


class FlaskAuthMail(AuthMail):
    def _send_email(self, subject, sender, recipients, text, html):
        msg = Message(subject, recipients=recipients, sender=sender)
        msg.text = text
        msg.html = html
        mail.send(msg)
        Thread(target=self._send_async_email, args=(mail.app, msg)).start()


    @staticmethod
    def _send_async_email(app, msg):
        with app.app_context():
            mail.send(msg)

    def send_password_recovery_message(self, user_email, recovery_code):
        self._send_email("Восстановление пароля",
           sender=mail.app.config['MAIL_DEFAULT_SENDER'],
           recipients=[user_email],
           text=render_template("email/recovery_password.txt", token=recovery_code),
           html=render_template("email/recovery_password.html", token=recovery_code)
       )

    def send_registration_message(self, user_email, registration_code):
        self._send_email("Подтверждение почты",
           sender=mail.app.config["MAIL_DEFAULT_SENDER"],
           recipients=[user_email],
           text=render_template("email/approve_email.txt", token=registration_code),
           html=render_template("email/approve_email.html", token=registration_code)
       )