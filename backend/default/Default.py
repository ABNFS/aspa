from typing import Optional, ClassVar, Any
from datetime import date, datetime

from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from sqlalchemy import select, Column, BIGINT, BOOLEAN, insert, Table, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session, declarative_base, declarative_mixin, declared_attr

from startup import SessionLocal

__db__: Session = None

Base = declarative_base()
__MAX_DEEP__: int = 4
__DEFAULT_DEEP__: int = 2


@declarative_mixin
class Mix:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    deleted = Column(BOOLEAN, default=False)

    def __str__(self):
        return f'{self.id}'

def objbase_to_dict(obj: Base, atual_deep: int = 0, max_deep: int = __MAX_DEEP__):
    # based in aswner https://stackoverflow.com/a/10664192/2638687
    atual_deep += 1
    if isinstance(obj.__class__, DeclarativeMeta):
        if atual_deep >= max_deep:
            return getattr(obj, "id", str(obj))
        dict_obj = dict()
        fields_to_translate = [x for x in dir(obj) if x not in ['deleted', 'metadata'] and x[0] != '_']
        for field in fields_to_translate:
            _obj_field = obj.__getattribute__(field)
            if isinstance(_obj_field, (date, datetime)):
                _obj_field = str(_obj_field)
            elif isinstance(_obj_field.__class__, DeclarativeMeta):
                _obj_field = convert_base_to_dict(_obj_field, atual_deep=atual_deep, max_deep=max_deep)
            elif isinstance(_obj_field, (list, tuple)):
                _list_obj_field: list | tuple = _obj_field
                _obj_field = []
                for _itens_obj_field in _list_obj_field:
                    if isinstance(_itens_obj_field.__class__, DeclarativeMeta):
                        _obj_field.append(
                            convert_base_to_dict(_itens_obj_field, atual_deep=atual_deep, max_deep=max_deep))
                    else:
                        _obj_field.append(str(_itens_obj_field))
            elif not isinstance(_obj_field, (str, int, dict)):
                continue
            dict_obj[field] = _obj_field

        return dict_obj
    else:
        return obj

def convert_base_to_dict(obj: Base | list, atual_deep: int = 0, max_deep: int = __MAX_DEEP__) -> dict | str | Any:
    if isinstance(obj, list):
        return [objbase_to_dict(o, atual_deep, max_deep) for o in obj]
    return objbase_to_dict(obj, atual_deep, max_deep)


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

    def get_all(self, db: Session, cls: ClassVar[Base]) -> list[Base]:
        result: list = []
        query = select(cls).where(cls.deleted.is_(False))
        for item in db.scalars(query):
            result.append(item)
        return result

    def raw_insert(self, db: Session, table: Table, **kwargs):
        stm = insert(table).values(**kwargs)
        db.execute(stm)
        db.commit()

    def raw_delete(self, db: Session, table: Table, **kwargs):
        stm = delete(table)
        for kw, args in kwargs.items():
            stm = stm.where(table.c[kw] == args)
        db.execute(stm)
        db.commit()

    def save(self, db: Session, data: Base) -> Base | None:
        db.add(data)
        try:
            db.commit()
        except IntegrityError:
            return None
        db.refresh(data)
        return data

    def search_by_name(self, db: Session, cls: ClassVar[Base], name: str = "") -> list[Base]:
        result: list = []
        query = select(cls).where(cls.name.ilike(f'%{name}%')).where(cls.deleted.is_(False))
        for account in db.scalars(query):
            result.append(account)
        return result
    def __map_dict_to_query(self, cls: ClassVar[Base], source: dict):
        query = select(cls).where(cls.deleted.is_(False))
        if isinstance(source, dict) or isinstance(cls, Base):
            for key, value in source.items():
                try:
                    if value or isinstance(value, bool):
                        attr = cls.__dict__[key]
                        if isinstance(value, str):
                            query = query.where(attr.ilike(f'%{value}%'))
                        elif isinstance(value, int):
                            query = query.where(attr == value)
                        elif isinstance(value, bool) or value is None:
                            query = query.where(attr.is_(value))
                        elif isinstance(value, (list, tuple)):
                            if isinstance(value[0], (date, datetime)):
                                query = query.where(attr.between(value[0], value[1]))
                            else:
                                query = query.where(attr.in_(value))
                        else:
                            query = query.where(attr.ilike(f'%{value}%'))
                except KeyError:
                    raise Exception('The field does not existe!')
            return query
        else:
            raise TypeError("I need a dict and a Base type")

    def search_by_fields(self, db: Session, cls: ClassVar[Base], fields: dict[str, Any]) -> list[Base]:
        result: list = []
        query = self.__map_dict_to_query(cls, fields)
        for item in db.scalars(query):
            result.append(item)
        return result

    def __get_by_id__(self, db: Session, cls: ClassVar[Base], id: int) -> Base:
        query = select(cls).where(cls.id == id).where(cls.deleted.is_(False))
        result = db.scalar(query)
        return result

    def __get_by_multiple_collum_id__(self, db: Session, cls: ClassVar[Base], id: dict) -> Base:
        query = self.__map_dict_to_query(cls, id)
        result = db.scalar(query)
        return result

    def get_by_id(self, db: Session, cls: ClassVar[Base], id: int) -> Base:
        return self.__get_by_id__(db, cls, id)

    def delete(self, db: Session, cls: ClassVar[Base], id: int | dict) -> bool:
        obj = None
        if isinstance(id, int):
            obj = self.__get_by_id__(db, cls, id)
        elif isinstance(id, dict):
            obj = self.__get_by_multiple_collum_id__(db, cls, id)
        if obj:
            obj.deleted = True
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj.deleted
        return False


class ServiceDefault:

    def __init__(self, database_class, repository: Optional[RepositoryDefault] = None):
        self.database_class = database_class
        self.repository = RepositoryDefault if repository else RepositoryDefault()

    def save(self, db: Session, data: DataModelDefault, max_deep: int=__DEFAULT_DEEP__):
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
        _saved: dict | None = convert_base_to_dict(self.repository.save(db, db_obj), max_deep=max_deep)
        if _saved:
            return _saved, status.HTTP_201_CREATED if new else status.HTTP_200_OK
        return {"code": "Erro", "text": "Integrity Database error, check your data"
                }, status.HTTP_400_BAD_REQUEST

    def search(self, db: Session, where_fields: dict[str, Any] | list[str | Any], max_deep: int = __DEFAULT_DEEP__):
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

        return convert_base_to_dict(selected, max_deep=max_deep) \
            , status.HTTP_200_OK if selected else status.HTTP_404_NOT_FOUND

    def get_all(self, db: Session, max_deep: int = __DEFAULT_DEEP__):
        return convert_base_to_dict(
            self.repository.get_all(db, self.database_class)
            , max_deep=max_deep), status.HTTP_200_OK

    def get(self, db: Session, id: int, max_deep: int = __DEFAULT_DEEP__):
        item = self.repository.get_by_id(db, self.database_class, id)
        return convert_base_to_dict(item, max_deep=max_deep), \
               status.HTTP_200_OK if item else status.HTTP_404_NOT_FOUND

    def delete(self, db: Session, id: int | dict):
        deleted = self.repository.delete(db, self.database_class, id)
        return deleted, status.HTTP_200_OK if deleted else status.HTTP_404_NOT_FOUND


class ControllerDefault:

    def __init__(self, service: Optional[ServiceDefault] = None):
        self.service: ServiceDefault = service
        self.db: Session = get_db()  # Session MUST be in Controller to don't expire data values

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
                    __item, _ = service.save(__db, item_data, max_deep=1)
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
