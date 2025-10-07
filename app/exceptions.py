from flask import Flask
from flask_limiter.errors import RateLimitExceeded
from werkzeug.exceptions import HTTPException, NotFound
import logging
from app.utils import respond

errors_string = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    409: "conflict",
    429: "too_many_requests",
    500: "internal_server_error",
}

class ApiException(Exception):
    status_code = 500

    def __init__(self, detail=None, status_code=None):
        self.status_code = status_code or self.status_code
        self.detail = detail


class ApiNotFound(ApiException):
    status_code = 404


class ApiBadRequest(ApiException):
    status_code = 400

class ApiUnauthorized(ApiException):
    status_code = 401

class ApiForbidden(ApiException):
    status_code = 403


def handle_exception(error):
    try:
        if isinstance(error, ApiException):
            return respond(
                error=errors_string.get(error.status_code, "unknown_error"),
                detail=error.detail,
                status_code=error.status_code,
            )
        elif isinstance(error, RateLimitExceeded):
            return respond(
                error=errors_string[429],
                detail={"rate": [error.description]},
                status_code=429
            )
        elif isinstance(error, HTTPException):
            status_code = getattr(error, "code", 500)
            return respond(
                error=errors_string[status_code],
                status_code=status_code
            )
        else:
            logging.error(error)
            return respond(
                error=errors_string[500],
                status_code=500
            )
    except KeyError as e:
        raise ValueError("Can't handle exception: {}".format(e))


def setup_exceptions(app: Flask):
    app.register_error_handler(Exception, handle_exception)