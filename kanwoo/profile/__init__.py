from flask import g
from werkzeug.local import LocalProxy

current_profile = LocalProxy(lambda: getattr(g, "_current_profile", None))