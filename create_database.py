from manage import *
from app.infrastructure.models.manga.sql_manga_adult import SQLMangaAdult
from app.infrastructure.models.manga.sql_manga_status import SQLMangaStatus
from app.infrastructure.models.manga.sql_manga_genre import SQLMangaGenre
from app.infrastructure.models.user.sql_user import SQLUser


from app.infrastructure.databases import sqlalchemy_db as db

with app.app_context():
    db.create_all()

    db.session.commit()