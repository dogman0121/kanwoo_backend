from flask import Blueprint
from app import limiter

bp = Blueprint('auth', __name__, url_prefix='/auth')

from .routes import *