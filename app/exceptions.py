from flask import Flask

from app.utils import respond

errors_string = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    409: "conflict",
    500: "internal_server_error",
}

class HTTPException(Exception):
    status_code = 500

    def __init__(self, detail=None, status_code=None):
        self.status_code = status_code or self.status_code
        self.detail = detail


class HTTPNotFound(HTTPException):
    status_code = 404


class HTTPBadRequest(HTTPException):
    status_code = 400


def handle_exception(error):
    try:
        if isinstance(error, HTTPException):
            return respond(
                error=errors_string[error.status_code],
                detail=error.detail,
                status_code=error.status_code,
            )
        else:
            print(error)
            return respond(
                error=errors_string[500],
                status_code=500
            )
    except KeyError as e:
        raise ValueError("Can't handle exception: {}".format(e))


def setup_exceptions(app: Flask):
    app.register_error_handler(Exception, handle_exception)