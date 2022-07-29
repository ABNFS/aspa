from typing import Optional, ClassVar, Any
from datetime import date, datetime

from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from sqlalchemy import select, Column, BIGINT, BOOLEAN, insert, Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session, declarative_base, declarative_mixin, declared_attr

from startup import SessionLocal

__db__: Session = None

Base = declarative_base()
__MAX_DEEP__: int = 4


@declarative_mixin
class Mix:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    deleted = Column(BOOLEAN, default=False)


def convert_base_to_dict(obj: Base, atual_deep: int = 0, max_deep: int = __MAX_DEEP__) -> dict | str | Any:
    # based in aswner https://stackoverflow.com/a/10664192/2638687
    atual_deep += 1
    if isinstance(obj.__class__, DeclarativeMeta):
        if atual_deep >= max_deep:
            return str(obj)
        dict_obj = dict()
        fields_to_translate = [x for x in dir(obj) if x not in ['deleted', 'metadata'] and x[0] != '_']
        for field in fields_to_translate:
            _obj_field = obj.__getattribute__(field)
            if isinstance(_obj_field, (date, datetime)):
                _obj_field = str(_obj_field)
            elif isinstance(_obj_field.__class__, (DeclarativeMeta, list, tuple)):
                _obj_field = convert_base_to_dict(_obj_field, atual_deep=atual_deep)
            elif not isinstance(_obj_field, (str, int, dict)):
                continue
            dict_obj[field] = _obj_field

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

    def get_all(self, db: Session, cls: ClassVar[Base]) -> list[dict]:
        result: list = []
        query = select(cls).where(cls.deleted.is_(False))
        for item in db.scalars(query):
            result.append(convert_base_to_dict(item))
        return result

    def raw_insert(self, db: Session, table: Table, commit: bool = True, **kwargs):
        stm = insert(table).values(**kwargs)
        db.execute(stm)
        if commit:
            db.commit()

    def save(self, db: Session, data: Base, commit: bool = True) -> dict | None:
        db.add(data)
        if commit:
            try:
                db.commit()
            except IntegrityError:
                return None
            db.refresh(data)
        return convert_base_to_dict(data)

    def search_by_name(self, db: Session, cls: ClassVar[Base], name: str = "") -> list:
        result: list = []
        query = select(cls).where(cls.name.ilike(f'%{name}%')).where(cls.deleted.is_(False))
        for account in db.scalars(query):
            result.append(convert_base_to_dict(account))
        return result

    def search_by_fields(self, db: Session, cls: ClassVar[Base], fields: dict[str, Any]) -> list:
        result: list = []
        query = select(cls).where(cls.deleted.is_(False))
        for field in fields:
            try:
                if fields[field] or isinstance(fields[field], bool):
                    attr = cls.__dict__[field]
                    value = fields[field]
                    if isinstance(value, str):
                        query = query.where(attr.ilike(f'%{fields[field]}%'))
                    elif isinstance(value, (int, bool)) or value is None:
                        query = query.where(attr.is_(fields[field]))
                    elif isinstance(value, list):
                        if isinstance(value[0], (date, datetime)):
                            query = query.where(attr.between(value[0], value[1]))
                        else:
                            query = query.where(attr.in_(value))
                    else:
                        query = query.where(attr.ilike(f'%{fields[field]}%'))
            except KeyError:
                raise Exception('The field does not existe!')
        for item in db.scalars(query):
            result.append(convert_base_to_dict(item))
        return result

    def __get_by_id__(self, db: Session, cls: ClassVar[Base], id: int):
        query = select(cls).where(cls.id == id).where(cls.deleted.is_(False))
        result = db.scalar(query)
        return result

    def get_by_id(self, db: Session, cls: ClassVar[Base], id: int):
        return convert_base_to_dict(self.__get_by_id__(db, cls, id))

    def delete(self, db: Session, cls: ClassVar[Base], id: int, commit: bool = True):
        obj = self.__get_by_id__(db, cls, id)
        if obj:
            obj.deleted = True
            db.add(obj)
            if commit:
                db.commit()
                db.refresh(obj)
            return obj.deleted
        return False


class ServiceDefault:

    def __init__(self, database_class, repository: Optional[RepositoryDefault] = None):
        self.database_class = database_class
        self.repository = RepositoryDefault if repository else RepositoryDefault()

    def save(self, db: Session, data: DataModelDefault):
        db_obj: Base
        new: bool = False
        if not data or not db:
            return {"code": "Erro", "text": "You MUST send a valid data"}, status.HTTP_400_BAD_REQUEST
        else:
            if not data.id or data.id < 0:
                new = True
                db_obj = self.database_class()
            else:
                db_obj = self.repository.__get_by_id__(db, self.database_class, data.id)

            for item in data.__dict__:
                try:
                    if not data.__getattribute__(item) is None:
                        db_obj.__setattr__(item, data.__getattribute__(item))
                except AttributeError:
                    pass
        _saved: dict | None = self.repository.save(db, db_obj)
        if _saved:
            return _saved, status.HTTP_201_CREATED if new else status.HTTP_200_OK
        return {"code": "Erro", "text": "Integrity Database error, check your data"
                }, status.HTTP_400_BAD_REQUEST

    def search(self, db: Session, where_fields: dict[str, str] | list[str | int]):
        """"
            call Repository with fields to search,
            :where_fields: may be a dict with:
                ::key = name of fiel in databse
                ::value = value for this fiel, if you need a between date or datetime, value MUST be a list with start
                and end date/time (SHOULD this sequence)
            Eventualy where_fields can a list with a name of the fiel in first position of this list, and a sequence of
            values in trail.
        """
        selected: list

        if isinstance(where_fields, list):
            key = where_fields[0:1][0]
            list_with_values = where_fields[1:len(where_fields)]
            where_fields = {key: list_with_values}
        if isinstance(where_fields, dict):
            selected = self.repository.search_by_fields(db, self.database_class, where_fields)
        else:
            selected = self.repository.get_all(db, self.database_class)

        return selected, status.HTTP_200_OK if selected else status.HTTP_404_NOT_FOUND

    def get_all(self, db: Session):
        res: list[Base] = []
        for data in self.repository.get_all(db, self.database_class):
            res.append(data)
        return res, status.HTTP_200_OK

    def get(self, db: Session, id: int):
        item = self.repository.get_by_id(db, self.database_class, id)
        return item, status.HTTP_200_OK if item else status.HTTP_404_NOT_FOUND

    def delete(self, db: Session, id: int):
        deleted = self.repository.delete(db, self.database_class, id)
        return deleted, status.HTTP_200_OK if deleted else status.HTTP_404_NOT_FOUND


class ControllerDefault:

    def __init__(self, service: Optional[ServiceDefault] = None):
        self.service: ServiceDefault = service
        self.db: Session = get_db() # Session MUST be in Controller to don't expire data values

    def new(self, service: Optional[ServiceDefault] = None,
            data: DataModelDefault | list[DataModelDefault] = None,
            message: Optional[dict[str, str]] = None):
        _status: int
        save_return_data: list | dict[str, str]
        if service is None:
            service = self.service
        if message is None:
            message = {"code": "Erro", "text": "Not found"}
        if data:
            save_return_data = []

            __db: Session = get_db()
            _status: int
            if isinstance(data, list):
                _status = status.HTTP_200_OK
                for item_data in data:
                    __item, _ = service.save(__db, item_data)
                    save_return_data.append(__item)
            else:
                __item, _status = service.save(__db, data)
                save_return_data.append(__item)
        else:
            _status = status.HTTP_404_NOT_FOUND
            save_return_data = message
        return JSONResponse(save_return_data, status_code=_status)

    def search(self, service: Optional[ServiceDefault] = None, name: Optional[str] = "", id: Optional[int] = -1,
               free_fields: dict = {},
               message: Optional[dict[str, str]] = None):

        db: Session = get_db()

        if service is None:
            service = self.service

        if message is None:
            message = {"code": "Erro", "text": "Not found"}

        _item: DataModelDefault
        _status: int

        if id >= 0:
            _item, _status = service.get(db, id)
        elif name:
            _item, _status = service.search(db, free_fields | {"name": name})
        elif free_fields:
            _item, _status = service.search(db, free_fields)
        else:
            _item, _status = service.get_all(db)

        return JSONResponse(message if _status == status.HTTP_404_NOT_FOUND else _item, status_code=_status)

    def delete(self, service: Optional[ServiceDefault] = None, id: Optional[int] = -1,
               message_sucess: dict[str, str] = None,
               message_fail: Optional[dict[str, str]] = None):
        if service is None:
            service = self.service

        if message_sucess is None:
            message_sucess = {"code": "Ok", "text": f"Think with {id} deleted"}

        if message_fail is None:
            message_fail = {"code": "Erro", "text": f"Imposible to delete think with {id}"}

        _db: Session = get_db()
        _deleted, _status = service.delete(_db, id)

        return JSONResponse(message_sucess if _deleted else message_fail, status_code=_status)
