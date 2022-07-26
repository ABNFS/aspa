from typing import ClassVar, Any

from sqlalchemy import select
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class GenericsRepository:

    @staticmethod
    def get_all(db: Session, cls: ClassVar) -> list:
        result: list = []
        query = select(cls).where(cls.deleted == False)
        for account in db.scalars(query):
            result.append(account)
        return result

    @staticmethod
    def save(db: Session, data: Base) -> Base:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    @staticmethod
    def search_by_name(db: Session, cls: ClassVar, name: str = "") -> list:
        result: list = []
        query = select(cls).where(cls.name.ilike(f'%{name}%')).where(cls.deleted == False)
        for account in db.scalars(query):
            result.append(account)
        return result

    @staticmethod
    def get_by_id(db: Session, cls: ClassVar, id: int):
        query = select(cls).where(cls.id == id).where(cls.deleted == False)
        result = db.scalar(query)
        return result

    @staticmethod
    def delete(db: Session, cls: ClassVar, id: int):
        obj = GenericsRepository.get_by_id(db, cls, id)
        if obj:
            obj.deleted = True
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj.deleted
        return False
