from kanwoo import db
from manage import app
from sqlalchemy import text

from kanwoo.chapter.models import Page

with app.app_context():
    # m = Manga.query.filter_by(id=7).scalar()
    # m.is_featured = True
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

    # db.session.execute(text("""DELETE FROM alembic_version;"""))
    # db.session.execute(text("""UPDATE profile SET role=30 WHERE slug='ivan';"""))

    for chapter in Page.query.all():
        chapter.path = f"pages/{chapter.uuid}.webp"


    db.session.commit()