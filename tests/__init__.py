class TestConfig:
    SECRET_KEY = "1234567890"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:12345678@localhost:5432/test"
    CACHE_URI = "redis://localhost:6379"

    COOKIE_DOMAIN = "localhost"
    ACCESS_COOKIE_NAME = "access_token_cookie"
    REFRESH_COOKIE_NAME = "refresh_token_cookie"
    ACCESS_CSRF_COOKIE_NAME = "csrf_access_token"
    REFRESH_CSRF_COOKIE_NAME = "csrf_refresh_token"
    AUTH_PROFILE_COOKIE_NAME = "auth_profile"

    JWT_TOKEN_LOCATION="cookies"
    JWT_COOKIE_DOMAIN = "localhost"
    JWT_COOKIE_SAMESITE = "None"
    JWT_COOKIE_SECURE = False
    JWT_REFRESH_COOKIE_PATH="/v1/refresh"
    JWT_REFRESH_CSRF_COOKIE_PATH="/v1/refresh"

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