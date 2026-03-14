class TestConfig:
    SECRET_KEY = "1234567890"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"

    JWT_COOKIE_DOMAIN = "localhost"
    JWT_COOKIE_SAMESITE = "None"
    JWT_COOKIE_SECURE = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'giachetti101@gmail.com'
    MAIL_DEFAULT_SENDER = 'giachetti101@gmail.com'
    MAIL_PASSWORD = 'dcnm jflp femx yuev'

    SERVER_NAME = "localhost:5000"
    USE_SSL = False

    UPLOAD_DIR = 'kanwoo/static'
    LOG_DIR = 'kanwoo/logs'

    CDN_URL = 'http://localhost:5000/static/'

    SERVER_DOMAIN = 'localhost'