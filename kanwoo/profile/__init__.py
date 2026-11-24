from flask import g
from werkzeug.local import LocalProxy

def get_current_profile():
    return g.current_profile

current_profile = LocalProxy(get_current_profile)