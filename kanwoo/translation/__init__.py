from flask import Blueprint

bp = Blueprint('translation', __name__, url_prefix='/translations')

import app.translation.routes