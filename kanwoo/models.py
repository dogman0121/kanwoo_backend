from sqlalchemy.orm import Mapped, mapped_column

from app import db

from datetime import datetime

import enum

class Base(db.Model):
    __abstract__ = True

    @classmethod
    def get(cls, entity_id):
        return db.session.get(cls, entity_id)

    def add(self, commit=True):
        db.session.add(self)

        if commit:
            db.session.commit()

    def update(self, data, commit=True):
        for key, value in data.items():
            setattr(self, key, value)

        if commit:
            db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)

        if commit:
            db.session.commit()

    def save(self):
        db.session.commit()


class File:
    __abstract__ = True

    uuid: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    orig_filename: Mapped[str] = mapped_column(nullable=True)
    ext: Mapped[str] = mapped_column(nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda x: datetime.now())
    is_deleted: Mapped[bool] = mapped_column(nullable=True, default=False)