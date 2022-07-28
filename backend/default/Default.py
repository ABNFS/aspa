from typing import Optional, ClassVar, Any

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select, Column, BIGINT, BOOLEAN
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session, declarative_base, declarative_mixin, declared_attr

from startup import SessionLocal

__db__: Session = None

Base = declarative_base()


@declarative_mixin
class Mix:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    deleted = Column(BOOLEAN, default=False)


__visited_objs__ = []


def make_dict(obj: Base):
    # based in aswner https://stackoverflow.com/a/10664192/2638687
    global __visited_objs__

    if isinstance(obj.__class__, DeclarativeMeta):
        if id(obj) in __visited_objs__:
            return None
        __visited_objs__.append(id(obj))

        dict_obj = {}
        for field in [x for x in obj.__dict__ if not x.startswith('_') and x != 'metadata' and x != 'deleted']:
            dict_obj[field] = obj.__getattribute__(field)
        return dict_obj
    return obj


def get_db():
    global __db__

    def get_session():
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    if (__db__ is None) or (not __db__.is_active):
        __db__ = next(get_session())
    return __db__


class DataModelDefault(BaseModel):
    id: Optional[int]

    class Config:
        orm_model: bool = True


class MessageDataDefault(DataModelDefault):
    code: Optional[str] = "Ok"
    text: Optional[str] = "Sucess"


class RepositoryDefault:

    def get_all(self, db: Session, cls: ClassVar[Base]) -> list:
        result: list = []
        query = select(cls).where(cls.deleted == False)
        for account in db.scalars(query):
            result.append(make_dict(account))
        return result

    def save(self, db: Session, data: Base) -> str:
        db.add(data)
        db.commit()
        db.refresh(data)
        return make_dict(data)

    def search_by_name(self, db: Session, cls: ClassVar[Base], name: str = "") -> list:
        result: list = []
        query = select(cls).where(cls.name.ilike(f'%{name}%')).where(cls.deleted == False)
        for account in db.scalars(query):
            result.append(make_dict(account))
        return result

    def search_by_str_fields(self, db: Session, cls: ClassVar[Base], fields: dict[str, Any]) -> list:
        result: list = []
        query = select(cls).where(cls.deleted == False)
        for field in fields:
            try:
                if fields[field] or isinstance(fields[field], bool):
                    attr = cls.__dict__[field]
                    if isinstance(attr, str):
                        query = query.where(attr.ilike(f'%{fields[field]}%'))
                    elif isinstance(attr, int) or isinstance(attr, bool):
                        query = query.where(attr == fields[field])
                    else:
                        query = query.where(attr.ilike(f'%{fields[field]}%'))
            except KeyError:
                raise Exception('The field does not existe!')
        for item in db.scalars(query):
            result.append(make_dict(item))
        return result

    def __get_by_id__(self, db: Session, cls: ClassVar[Base], id: int):
        query = select(cls).where(cls.id == id).where(cls.deleted == False)
        result = db.scalar(query)
        return result

    def get_by_id(self, db: Session, cls: ClassVar[Base], id: int):
        return make_dict(self.__get_by_id__(db, cls, id))

    def delete(self, db: Session, cls: ClassVar[Base], id: int):
        obj = self.__get_by_id__(db, cls, id)
        if obj:
            obj.deleted = True
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj.deleted
        return False


class ServiceDefault:
    database_class: ClassVar
    repository: RepositoryDefault

    def __init__(self, database_class: ClassVar, repository: Optional[RepositoryDefault] = None):
        self.database_class = database_class
        self.repository = RepositoryDefault if repository else RepositoryDefault()

    def save(self, db: Session, data: DataModelDefault):
        db_obj: Base
        if not data.id or data.id < 0:
            db_obj = self.database_class()
        else:
            db_obj = self.repository.__get_by_id__(db, self.database_class, data.id)

        for item in data.__dict__:
            try:
                if not data.__getattribute__(item) is None:
                    db_obj.__setattr__(item, data.__getattribute__(item))
            except AttributeError:
                pass
        return self.repository.save(db, db_obj)

    def search(self, db: Session, search_dict: dict[str, str]):
        return self.repository.search_by_str_fields(db, self.database_class, search_dict)

    def get_all(self, db: Session):
        res: list[Base] = []
        for data in self.repository.get_all(db, self.database_class):
            res.append(data)
        return res

    def get(self, db: Session, id: int):
        return self.repository.get_by_id(db, self.database_class, id)

    def delete(self, db: Session, id: int):
        return self.repository.delete(db, self.database_class, id)


class ControllerDefault:
    service: ServiceDefault

    def __init__(self, service: Optional[ServiceDefault] = None):
        self.service = service

    def new(self, service: Optional[ServiceDefault] = None,
            data: DataModelDefault | list[DataModelDefault] = None,
            message: Optional[dict[str, str]] = None):
        if service is None:
            service = self.service
        if message is None:
            message = {"code": "Erro", "text": "Not found"}
        if data:
            save_return_data: list[DataModelDefault] = []

            db: Session = get_db()

            if isinstance(data, list):
                for item_data in data:
                    save_return_data.append(service.save(db, item_data))
            else:
                save_return_data.append(service.save(db, data))
            return JSONResponse(save_return_data)
        else:
            return JSONResponse(message, status_code=404)

    def search(self, service: Optional[ServiceDefault] = None, name: Optional[str] = "", id: Optional[int] = -1,
               free_fields: dict = None,
               message: Optional[dict[str, str]] = None):

        db: Session = get_db()

        if service is None:
            service = self.service

        if message is None:
            message = {"code": "Erro", "text": "Not found"}

        if free_fields:
            return JSONResponse(service.search(db, free_fields))
        elif id < 0:
            return JSONResponse(service.search(db, {"name": name}))
        else:
            item = service.get(db, id)
            if item:
                return JSONResponse(item)
            return JSONResponse(message, status_code=400)

    def delete(self, service: Optional[ServiceDefault] = None, id: Optional[int] = -1, message_sucess: dict[str, str] = None,
               message_fail: Optional[dict[str, str]] = None):
        if service is None:
            service = self.service

        if message_sucess is None:
            raise Exception("You CAN send a message")

        if message_fail is None:
            message_fail = {"code": "Erro", "text": f"Imposible to delete {id}"}

        db: Session = get_db()

        if service.delete(db, id):
            return JSONResponse(message_sucess)
        return JSONResponse(message_fail, status_code=404)
