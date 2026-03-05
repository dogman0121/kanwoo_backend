

def setup_routes(app):
    from kanwoo.auth.routes import bp as auth_bp
    from kanwoo.manga.routes import bp as manga_bp
    from kanwoo.translation.routes import bp as translation_bp
    from kanwoo.chapter.routes import bp as chapter_bp
    from kanwoo.search.routes import bp as search_bp
    from kanwoo.comment import bp as comment_bp
    from kanwoo.list import bp as lists_bp
    from kanwoo.home.routes import bp as home_bp
    from kanwoo.main.routes import bp as main_bp
    from kanwoo.profile.routes import bp as profiles_bp
    from kanwoo.admin.routes import bp as admin_bp

    app.register_blueprint(main_bp, url_prefix="/v1")
    app.register_blueprint(search_bp, url_prefix='/v1/search')
    app.register_blueprint(comment_bp)
    app.register_blueprint(manga_bp, url_prefix="/v1/manga")
    app.register_blueprint(profiles_bp, url_prefix='/v1/profiles')
    app.register_blueprint(lists_bp, url_prefix='/v1/lists')
    app.register_blueprint(home_bp, url_prefix='/v1/home')
    app.register_blueprint(auth_bp, url_prefix='/v1/auth')
    app.register_blueprint(translation_bp, url_prefix='/v1/translations')
    app.register_blueprint(chapter_bp, url_prefix='/v1/chapters')
    app.register_blueprint(admin_bp, url_prefix='/v1/admin')