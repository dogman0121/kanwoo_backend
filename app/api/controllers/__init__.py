from .home_routes import bp as home_bp

def setup_blueprints(app):
    app.register_blueprint(home_bp, url_prefix='/api/v1/home')

