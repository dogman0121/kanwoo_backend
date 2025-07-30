from flask import Blueprint

from app.api.schemas.home_schema import HomeSchema
from app.infrastructure.repositories.sql.sql_manga_repo import SQLMangaRepository
from app.use_cases.home.get_home_blocks import GetHomeBlocksUseCase
from app.utils import create_response

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('', methods=['GET'], strict_slashes=False)
def get_home():
    schema = HomeSchema()

    res = GetHomeBlocksUseCase(manga_repo=SQLMangaRepository()).execute()

    data = schema.dump(res)

    return create_response(data=data, status_code=200)
