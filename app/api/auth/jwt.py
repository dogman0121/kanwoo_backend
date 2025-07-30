from flask_jwt_extended import JWTManager

from app.api.responses import create_response

jwt_manager = JWTManager()

def setup_jwt_manager(app):
    jwt_manager.init_app(app)

    @jwt_manager.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return create_response(error="unauthorized", detail={"token": "Token expired"}), 401

    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error):
        return create_response(error="unauthorized", detail={"token": "Invalid token"}), 401

    @jwt_manager.unauthorized_loader
    def unauthorized_callback(error):
        return create_response(error="unauthorized", detail={"token": "Missing authorization token"}), 401