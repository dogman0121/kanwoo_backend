import uuid

from app import db
from app.manga.models import Type, Status, Genre, Adult, Manga
from manage import app
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    m = Manga.query.filter_by(id=7).scalar()
    m.is_featured = True
    # s = Status(name="нет")
    # t = Type(name="нет")
    # g1 = Genre(name="драки")
    # g2 = Genre(name="романтика")
    # a = Adult(name="нет")

    # s.add()
    # t.add()
    # g1.add()
    # g2.add()
    # a.add()

    # db.session.execute(text("DELETE FROM notification;"))

    db.session.commit()