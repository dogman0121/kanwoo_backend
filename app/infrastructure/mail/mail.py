from flask_mail import Mail

mail = Mail()

def setup_mail(app):
    MailAdapter(app)

class MailAdapter:
    def __init__(self, app):
        mail.init_app(app)