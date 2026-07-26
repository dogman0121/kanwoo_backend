from flask import jsonify, current_app

def respond(
    data=None, 
    error=None, 
    detail=None, 
    metadata=None, 
    status_code=200,
    page=None,
    per_page=None,
    last_id=None,
    limit=None,
    total_count=None
):
    response_dict = {}

    if error:
        response_dict["error"] = {
            "code": error,
            "detail": detail,
        }
    else:
        response_dict["data"] = data
        response_dict["metadata"] = metadata

        if page is not None:
            response_dict["pagination"] = {
                "page": page,
                "per_page": per_page,
                "total_count": total_count
            }
        elif last_id is not None:
            response_dict["pagination"] = {
                "last_id": last_id,
                "limit": limit
            }


    response = jsonify(response_dict)

    response.status_code = status_code

    return response