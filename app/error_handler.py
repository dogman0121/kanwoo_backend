def setup_error_handler(app) -> None:
    def error_handler(error):
        return "Internal Server Error", 500

    return app.errorhandler(Exception)(error_handler)