

def setup_routes(app):
    from app.user import bp as user_bp
    from app.search import bp as search_bp
    from app.comments import bp as comment_bp
    from app.chapters import bp as chapters_bp
    from app.manga import bp as manga_bp
    from app.team import bp as teams_bp
    from app.notifications import bp as notifications_bp
    from app.lists import bp as lists_bp
    from app.home import bp as home_bp
    from app.auth import bp as auth_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(chapters_bp, url_prefix='/api/v1/chapters')
    app.register_blueprint(manga_bp, url_prefix="/api/v1/manga")
    app.register_blueprint(teams_bp, url_prefix='/api/v1/teams')
    app.register_blueprint(notifications_bp, url_prefix='/api/v1/notifications')
    app.register_blueprint(lists_bp, url_prefix='/api/v1/lists')
    app.register_blueprint(home_bp, url_prefix='/api/v1/home')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')