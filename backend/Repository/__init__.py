from typing import ClassVar, Any, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session, declarative_base, DeclarativeMeta

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
    def search_by_str_fields(db: Session, cls: ClassVar, fields: Dict[str, str]) -> list:
        result: list = []
        query = select(cls).where(cls.deleted == False)
        for field in fields:
            try:
                if fields[field]:
                    attr = cls.__dict__[field]
                    query = query.where(attr.ilike(f'%{fields[field]}%'))
            except KeyError:
                raise Exception('The field does not existe!')
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
