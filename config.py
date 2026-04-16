import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    CACHE_URI = os.getenv("CACHE_URI")

    JWT_SESSION_COOKIE = False
    JWT_CSRF_IN_COOKIES = True
    JWT_TOKEN_LOCATION = "cookies"
    JWT_VERIFY_SUB = False
    JWT_COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN")
    JWT_COOKIE_SAMESITE = None
    JWT_COOKIE_SECURE = True
    JWT_ACCESS_COOKIE_NAME = os.getenv("ACCESS_COOKIE_NAME")
    JWT_REFRESH_COOKIE_NAME = os.getenv("REFRESH_COOKIE_NAME")
    JWT_ACCESS_CSRF_COOKIE_NAME = os.getenv("ACCESS_CSRF_COOKIE_NAME")
    JWT_REFRESH_CSRF_COOKIE_NAME = os.getenv("ACCESS_CSRF_COOKIE_NAME")


    MAIL_USE_TLS = True
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    UPLOAD_DIR = "kanwoo/static"
    LOG_DIR = "kanwoo/log"

    DOMAIN = os.environ.get("DOMAIN")
    CDN_URL = os.environ.get("CDN_URL")
    FRONTEND_URL = os.environ.get("FRONTEND_URL")