from flask import Blueprint

bp = Blueprint('manga', __name__, url_prefix='/manga')

import app.manga.routes