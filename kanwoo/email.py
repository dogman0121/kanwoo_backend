from threading import Thread
from flask_mail import Message
from flask import render_template, current_app
from kanwoo import mail
from kanwoo.user.models import User


def _send_email(subject, sender, recipients, text, html):
    msg = Message(subject, recipients=recipients, sender=sender)
    msg.text = text
    msg.html = html
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

class EmailService:
    def send_email(self, subject, recipients, text, html):

        _send_email(
            subject,
            current_app.config["MAIL_DEFAULT_SENDER"],
            recipients,
            text,
            html
        )


def send_password_recovery_mail(user_id, email):
    token = User.get_by_id(user_id).get_recovery_token()
    _send_email("Восстановление пароля",
               sender=current_app.config["MAIL_DEFAULT_SENDER"],
               recipients=[email],
               text=render_template("email/recovery_password.txt", token=token),
               html=render_template("email/recovery_password.html", token=token)
               )

def send_registration_verification_mail(login, email, password):
    token = User.get_registration_token(login, email, password)
    _send_email("Подтверждение почты",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email],
        text=render_template("email/approve_email.txt", token=token),
        html=render_template("email/approve_email.html", token=token)
    )