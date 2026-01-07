

def setup_routes(app):
    from app.user import bp as user_bp
    from app.search import bp as search_bp
    from app.comment import bp as comment_bp
    from app.chapter import bp as chapter_bp
    from app.manga import bp as manga_bp
    from app.profile import bp as profiles_bp
    from app.list import bp as lists_bp
    from app.home import bp as home_bp
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    from app.translation import bp as translation_bp

    app.register_blueprint(main_bp, url_prefix="/v1")
    app.register_blueprint(user_bp)
    app.register_blueprint(search_bp, url_prefix='/v1/search')
    app.register_blueprint(comment_bp)
    app.register_blueprint(manga_bp, url_prefix="/v1/manga")
    app.register_blueprint(profiles_bp, url_prefix='/v1/profiles')
    app.register_blueprint(lists_bp, url_prefix='/v1/lists')
    app.register_blueprint(home_bp, url_prefix='/v1/home')
    app.register_blueprint(auth_bp, url_prefix='/v1/auth')
    app.register_blueprint(translation_bp, url_prefix='/v1/translations')
    app.register_blueprint(chapter_bp, url_prefix='/v1/chapters')