from flask import jsonify, current_app

def respond(data=None, error=None, detail=None, metadata=None, status_code=200):
    if error:
        response = jsonify({
            "error": {
                "code": error,
                "detail": detail,
            }
        })
    else:
        response = jsonify({
            "data": data,
            "metadata": metadata
        })

    response.status_code = status_code

    return response