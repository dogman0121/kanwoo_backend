from sqlalchemy import func, select, or_, and_, asc, desc
from sqlalchemy.orm import Mapped, mapped_column, Query, Session
from typing import Optional

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

def cursor_paginate(
    cls, 
    session: Session, 
    query: Query, 
    sort_field: Optional[str] = None,
    cursor: Optional[dict] = None, 
    limit: Optional[int] = 10, 
    direction: str = "asc"
):
    res_q = query

    if sort_field:
        sort_attr = getattr(cls, sort_field)
    else:
        sort_attr = None

    if cursor:
        last_id = cursor.get("id")
        last_sort_field_val = cursor.get(sort_field)

        if last_sort_field_val:
            if direction == "asc":
                res_q = res_q.filter(
                    or_(
                        sort_attr > last_sort_field_val,
                        and_(cls.id > last_id, sort_attr == last_sort_field_val)
                    )
                )
            elif direction == "desc":
                res_q = res_q.filter(
                    or_(
                        sort_attr < last_sort_field_val,
                        and_(cls.id < last_id, sort_attr == last_sort_field_val)
                    )
                )
        else:
            if direction == "asc":
                res_q = res_q.filter(cls.id > last_id)
            elif direction == "desc":
                res_q = res_q.filter(cls.id < last_id)
    

    if direction == "asc":
        if sort_attr:
            res_q = res_q.order_by(asc(sort_attr))

        res_q = res_q.order_by(asc(cls.id))
    else:
        if sort_attr:
            res_q = res_q.order_by(desc(sort_attr))

        res_q = res_q.order_by(desc(cls.id))


    results = session.execute(res_q.limit(limit+1)).unique().scalars().all()
    has_more = len(results) > limit

    if has_more:
        results = results[:limit]

    if len(results):
        new_cursor = {
            "id": results[-1].id
        }

        if sort_field:
            getattr(results[-1], sort_field)
    else:
        new_cursor = cursor

    return results[: limit], new_cursor, has_more