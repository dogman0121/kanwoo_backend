from sqlalchemy import func, select
from sqlalchemy.orm import Mapped, mapped_column, Query, Session


from kanwoo import db, file_storage

from datetime import datetime

class Base(db.Model):
    __abstract__ = True

    @classmethod
    def get(cls, entity_id):
        return db.session.get(cls, entity_id)

    def add(self, commit=False):
        db.session.add(self)

        if commit:
            db.session.commit()

    def update(self, data, commit=False):
        for key, value in data.items():
            setattr(self, key, value)

        if commit:
            db.session.commit()

    def delete(self, commit=False):
        db.session.delete(self)

        if commit:
            db.session.commit()

    def save(self):
        db.session.commit()


class File:
    __abstract__ = True

    uuid: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    path: Mapped[str] = mapped_column(nullable=True)
    orig_filename: Mapped[str] = mapped_column(nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda x: datetime.now())
    is_deleted: Mapped[bool] = mapped_column(nullable=True, default=False)

    def delete(self):
        self.is_deleted = True

    def __str__(self):
        return file_storage.get_url(self.path)


class Privacy(Base):
    __tablename__ = "privacy"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()

class Language(Base):
    __tablename__ = "language"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()


def page_paginate(session: Session, query: Query, page: int, per_page: int):
    total_count = session.execute(select(func.count("*")).select_from(query)).scalar()
    results = session.execute(query.offset((page-1)*per_page).limit(per_page)).unique().scalars().all()

    return results, total_count

def cursor_paginate(cls, session: Session, query: Query, last_id: int, limit: int):
    total_count = session.execute(select(func.count("*")).select_from(query)).scalar()
    results = session.execute(query.filter(cls.id > last_id).limit(limit)).unique().scalars().all()

    if results != []:    
        last_id = results[-1].id
    else:
        last_id = 0

    return results, total_count, last_id