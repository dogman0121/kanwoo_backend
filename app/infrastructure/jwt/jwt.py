class JWT:
    app = None

    def __init__(self, app=None):
        self.app = app

    def init_app(self, app):
        if app.config.get('JWT_SECRET') is None:
            raise RuntimeError('JWT_SECRET must be set')

        self.app = app


jwt = JWT()

def setup_jwt(app):
    JWTAdapter(app)

class JWTAdapter(object):
    def __init__(self, app):
        jwt.init_app(app)

