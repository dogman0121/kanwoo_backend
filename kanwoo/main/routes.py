from . import bp
from .schemas import MetaSchema

from app.utils import respond
from app.manga.models import Genre, Status, Adult, Type

@bp.route("/meta", methods=["GET"])
def get_meta_route():
    statuses = Status.query.all()
    types = Type.query.all()
    genres = Genre.query.all()
    adults = Adult.query.all()

    schema = MetaSchema()

    return respond(data=schema.dump({
        "statuses": statuses,
        "types": types,
        "genres": genres,
        "adults": adults
    }))