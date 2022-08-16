from typing import Callable, Optional, ClassVar, Any
from datetime import date, datetime
from pathlib import Path
from os import getenv
from yaml import safe_load
from logging import getLogger, Logger, StreamHandler, Formatter

from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from sqlalchemy import select, Column, BIGINT, BOOLEAN, insert, Table, delete, create_engine
from sqlalchemy.future import Engine
from sqlalchemy.exc import DatabaseError, OperationalError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session, declarative_base, declarative_mixin, declared_attr, sessionmaker

_DATABASE_URL_ENV_NAME = 'DATABASE_URL'
_CONFIG_FILE_ENV_NAME = 'CONFIG_FILE_PATH'
_FILE: str = './config.yaml'

_DEFAULT_LEVEL: str = 'ERROR'

__database_url__: str = ''
__database_engine__: Engine | None = None
__SessionLocal__: Callable | None = None
__db__: Session | None = None

Base = declarative_base()
MAX_DEEP: int = 4
DEFAULT_DEEP: int = 2
log: Logger | None = None


def __get_yaml_dict(path_to_file: Optional[Path] = None) -> dict[str:Any]:
    def get_config_file_from_env() -> Path:
        return Path(getenv(_CONFIG_FILE_ENV_NAME, _FILE))

    yaml_confs: dict[str:Any]
    if path_to_file is None:
        path_to_file = get_config_file_from_env()
    try:
        yaml_confs = safe_load(open(path_to_file))
        if 'database' not in yaml_confs:
            yaml_confs['database'] = {}
    except FileNotFoundError:
        yaml_confs = {'database': {}}
    return yaml_confs


def get_from_conf(key: str, default_value: Optional[Any] = None, section: Optional[str] = "",
                  path_to_file: Optional[Path] = None) -> Any:
    conf = __get_yaml_dict(path_to_file)
    value: Any
    if section:
        value = conf[section][key] if section in conf and key in conf[section] else default_value
    else:
        value = conf[key] if key in conf else default_value
    return value


def __startup__(path: Optional[Path] = None) -> None:
    global __database_url__, __database_engine__, __SessionLocal__, log

    def _get_logger(level) -> Logger:
        _log = getLogger('DFW')
        _log.setLevel(level)
        stream_handler = StreamHandler()
        stream_handler.setLevel(level)
        formatter = Formatter('%(levelname)s: %(message)s - %(name)s (%(asctime)s)')
        stream_handler.setFormatter(formatter)
        _log.addHandler(stream_handler)
        return _log

    def make_url_db_from_config_file(path_to_file: Optional[Path] = None) -> str:
        yaml_confs = __get_yaml_dict(path_to_file)
        _drive = 'sqlite' if "drive" not in yaml_confs['database'] else f"{yaml_confs['database']['drive']}"
        _user = '' if "user" not in yaml_confs['database'] else f"{yaml_confs['database']['user']}:"
        _password = '' if "password" not in yaml_confs['database'] else f"{yaml_confs['database']['password']}@"
        _url = '' if "url" not in yaml_confs['database'] else f"{yaml_confs['database']['url']}/"
        _name = 'dev.db' if "name" not in yaml_confs['database'] else yaml_confs['database']['name']

        return f'{_drive}://{_user}{_password}{_url}{_name}?charset=utf8'

    logger_level: str = get_from_conf(section='log', key='level', default_value=_DEFAULT_LEVEL).upper()
    _DEBUG: bool = logger_level == "DEBUG"
    __database_url__ = getenv(_DATABASE_URL_ENV_NAME, make_url_db_from_config_file(path))
    __drive = __database_url__.split(':')[0]
    if __drive == "sqlite":
        __database_engine__ = create_engine(__database_url__, echo=_DEBUG, future=True,
                                            connect_args={"check_same_thread": False})
    else:
        __database_engine__ = create_engine(__database_url__, echo=_DEBUG, future=True)

    __SessionLocal__ = sessionmaker(bind=__database_engine__, autocommit=False, autoflush=False, expire_on_commit=True)
    log = _get_logger(logger_level)


class DefaultError(BaseException):
    message: str

    def __init__(self, message, *args, **kwargs):
        super(*args, **kwargs)
        self.message = message


class RepositoryError(DefaultError):
    pass


class ServiceError(DefaultError):
    pass


class ControllerError(DefaultError):
    pass


@declarative_mixin
class Mix:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    deleted = Column(BOOLEAN, default=False)

    def __str__(self):
        return f'{self.id}'


async def objbase_to_dict(obj: Base, atual_deep: int = 0, max_deep: int = MAX_DEEP):
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
                _obj_field = await convert_base_to_dict(_obj_field, atual_deep=atual_deep, max_deep=max_deep)
            elif isinstance(_obj_field, (list, tuple)):
                _list_obj_field: list | tuple = _obj_field
                _obj_field = []
                for _itens_obj_field in _list_obj_field:
                    if isinstance(_itens_obj_field.__class__, DeclarativeMeta):
                        _obj_field.append(
                            await convert_base_to_dict(_itens_obj_field, atual_deep=atual_deep, max_deep=max_deep))
                    else:
                        _obj_field.append(str(_itens_obj_field))
            elif not isinstance(_obj_field, (str, int, dict)):
                continue
            dict_obj[field] = _obj_field

        return dict_obj
    else:
        return obj


async def convert_base_to_dict(obj: Base | list, atual_deep: int = 0, max_deep: int = MAX_DEEP) -> dict | str | Any:
    if isinstance(obj, list):
        return [await objbase_to_dict(o, atual_deep, max_deep) for o in obj]
    return await objbase_to_dict(obj, atual_deep, max_deep)


async def get_db():
    global __db__

    def get_session():
        session = __SessionLocal__()
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

    async def get_all(self, db: Session, cls: ClassVar[Table]) -> list[Base]:
        result: list = []
        query = select(cls).where(cls.deleted.is_(False))
        try:
            for item in db.scalars(query):
                result.append(item)
            return result
        except OperationalError as e:
            if log:
                log.info(f"{e.args[0]}")
            raise RepositoryError(message="Database offline")

    async def raw_insert(self, db: Session, table: Table, **kwargs):
        try:
            stm = insert(table).values(**kwargs)
            db.execute(stm)
            db.commit()
        except OperationalError as e:
            if log:
                log.info(f"{e.args[0]}")
            raise RepositoryError(message="Database offline")

    async def raw_delete(self, db: Session, table: Table, **kwargs):
        try:
            stm = delete(table)
            for kw, args in kwargs.items():
                stm = stm.where(table.c[kw] == args)
            db.execute(stm)
            db.commit()
        except OperationalError as e:
            if log:
                log.info(f"{e.args[0]}")
            raise RepositoryError(message="Database offline")

    async def save(self, db: Session, data: Base) -> Base | None:
        try:
            db.add(data)
            try:
                db.commit()
            except DatabaseError as e:
                if log:
                    log.debug(f"Integrity error: {e.args[0]}")
                raise RepositoryError(message=f"Error on save data {e.code}")
            db.refresh(data)
            return data
        except OperationalError as e:
            if log:
                log.info(f"{e.args[0]}")
            raise RepositoryError(message="Database offline")

    async def __map_dict_to_query(self, cls: ClassVar[Base], source: dict):
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
                except KeyError as e:
                    if log:
                        log.debug(f"Field {key} not found {e.args}")

                    raise Exception('The field does not existe!')
            return query
        else:
            raise TypeError("I need a dict and a Base type")

    async def search_by_fields(self, db: Session, cls: ClassVar[Base], fields: dict[str, Any]) -> list[Base]:
        try:
            result: list = []
            query = await self.__map_dict_to_query(cls, fields)
            for item in db.scalars(query):
                result.append(item)
            return result
        except OperationalError as e:
            if log:
                log.info(f"{e.args[0]}")
            raise RepositoryError(message="Database offline")

    async def __get_by_id__(self, db: Session, cls: ClassVar[Base], id: int) -> Base:
        try:
            query = select(cls).where(cls.id == id).where(cls.deleted.is_(False))
            result = db.scalar(query)
            return result
        except OperationalError as e:
            if log:
                log.info(f"{e.args[0]}")
            raise RepositoryError(message="Database offline")

    async def __get_by_multiple_collum_id__(self, db: Session, cls: ClassVar[Base], id: dict) -> Base:
        try:
            query = await self.__map_dict_to_query(cls, id)
            result = db.scalar(query)
            return result
        except OperationalError as e:
            if log:
                log.info(f"{e.args[0]}")
            raise RepositoryError(message="Database offline")

    async def get_by_id(self, db: Session, cls: ClassVar[Base], id: int) -> Base:
        try:
            return await self.__get_by_id__(db, cls, id)
        except OperationalError as e:
            if log:
                log.info(f"Database offline - Code {e.args[0]}")
            raise RepositoryError(message="Database offline")

    async def delete(self, db: Session, cls: ClassVar[Base], id: int | dict) -> bool:
        try:
            obj = None
            if isinstance(id, int):
                obj = await self.__get_by_id__(db, cls, id)
            elif isinstance(id, dict):
                obj = await self.__get_by_multiple_collum_id__(db, cls, id)
            if obj:
                obj.deleted = True
                db.add(obj)
                db.commit()
                db.refresh(obj)
                return obj.deleted
            return False
        except OperationalError as e:
            if log:
                log.info(f"Database offline - Code {e.args[0]}")
            raise RepositoryError(message="Database offline")


class ServiceDefault:

    def __init__(self, database_class, repository: Optional[RepositoryDefault] = None):
        self.database_class = database_class
        self.repository = RepositoryDefault if repository else RepositoryDefault()

    async def __save__(self, db: Session, data: DataModelDefault, max_deep: int, db_obj: Base) -> dict:
        if not data or not db:
            if log:
                log.debug(f"Data invalid {data}")
            raise ServiceError(message="You MUST send a valid data")
        for item in data.__dict__:
            try:
                if not data.__getattribute__(item) is None:
                    db_obj.__setattr__(item, data.__getattribute__(item))
            except AttributeError:
                if log:
                    log.debug(f"Not found {item} in {data} or {db_obj}")
                pass

        try:
            _saved: dict | None = await convert_base_to_dict(await self.repository.save(db, db_obj), max_deep=max_deep)
        except RepositoryError as e:
            if log:
                log.debug(f"Integrity error: {e.message}")
            raise ServiceError(message="Integrity Database error, check your data")
        if not _saved:
            if log:
                log.debug(f"{data} not saved")
            raise ServiceError(message="No data saved")
        return _saved

    async def save(self, db: Session, data: DataModelDefault, max_deep: int = DEFAULT_DEEP) -> dict:
        db_obj: Base
        try:
            db_obj = await self.repository.__get_by_id__(db, self.database_class, data.id)
            return await self.__save__(db, data, max_deep, db_obj)
        except RepositoryError as e:
            if log:
                log.debug(f"Error from repository {e.message}. Generally your database is offline")
            raise ServiceError(message=f"DBError: {e.message}")

    async def new(self, db: Session, data: DataModelDefault, max_deep: int = DEFAULT_DEEP) -> dict:
        try:
            return await self.__save__(db, data, max_deep, self.database_class())
        except RepositoryError as e:
            if log:
                log.debug(f"Error form repository {e.message}. Generally your database is offline")
            raise ServiceError(message=f"DBError: {e.message}")

    async def search(self, db: Session, where_fields: dict[str, Any] | list[str | Any],
                     max_deep: int = DEFAULT_DEEP) -> dict:
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
        try:
            if isinstance(where_fields, dict):
                selected = await self.repository.search_by_fields(db, self.database_class, where_fields)
            else:
                selected = await self.repository.get_all(db, self.database_class)
        except RepositoryError as e:
            if log:
                log.debug(f"Error form repository {e.message}. Generally your database is offline")
            raise ServiceError(message=f"DBError: {e}")
        if not selected:
            raise ServiceError(message="Not Found")

        return await convert_base_to_dict(selected, max_deep=max_deep)

    async def get_all(self, db: Session, max_deep: int = DEFAULT_DEEP) -> list[dict]:
        try:
            return await convert_base_to_dict(await self.repository.get_all(db, self.database_class), max_deep=max_deep)
        except RepositoryError as e:
            if log:
                log.debug(f"Error form repository {e.message}. Generally your database is offline")
            raise ServiceError(message=f"DBError: {e}")

    async def get(self, db: Session, id: int, max_deep: int = DEFAULT_DEEP) -> dict:
        try:
            return await convert_base_to_dict(await self.repository.get_by_id(db, self.database_class, id),
                                              max_deep=max_deep)
        except RepositoryError as e:
            if log:
                log.debug(f"Error form repository {e.message}. Generally your database is offline")
            raise ServiceError(message=f"DBError: {e}")

    async def delete(self, db: Session, id: int | dict) -> bool:
        try:
            return await self.repository.delete(db, self.database_class, id)
        except RepositoryError as e:
            if log:
                log.debug(f"Error form repository {e.message}. Generally your database is offline")
            raise ServiceError(message=f"DBError: {e}")


class ControllerDefault:
    service: ServiceDefault

    def __init__(self, service: Optional[ServiceDefault] = None, database_class=None):
        if (service is None) and not (database_class is None):
            self.service = ServiceDefault(database_class=database_class)
        elif not (service is None):
            self.service: ServiceDefault = service
        else:
            if log:
                log.debug(f"Invalid service or database_class: {service}, {database_class}")
            raise ControllerError(message="You SHOULD send a valid service or database_class")

    async def __new_item(self, db, service, data, response: bool = True) -> dict | JSONResponse:
        __item: dict
        if not data.id or data.id < 0:
            __item = await service.new(db, data)
            if response:
                return JSONResponse(__item, status_code=status.HTTP_201_CREATED)
        else:
            __item = await service.save(db, data)
            if response:
                return JSONResponse(__item, status_code=status.HTTP_200_OK)
        return __item

    async def __new_list(self, db, service, list_data: list) -> JSONResponse:
        save_return_data = []
        for item_data in list_data:
            __item = await self.__new_item(db, service, item_data, response=False)
            save_return_data.append(__item)
        return JSONResponse(save_return_data, status_code=status.HTTP_200_OK)

    async def new(self, service: Optional[ServiceDefault] = None,
                  data: DataModelDefault | list[DataModelDefault] = None,
                  message: Optional[dict[str, str]] = None) -> JSONResponse:
        save_return_data: list | dict[str, str]
        if service is None:
            service = self.service
        if message is None:
            message = {"code": "Erro", "text": "Not found"}
        if data:
            __db: Session = await get_db()
            try:
                if isinstance(data, list):
                    return await self.__new_list(__db, service, data)
                else:
                    return await self.__new_item(__db, service, data)
            except ServiceError as e:
                return JSONResponse(e.message, status_code=status.HTTP_400_BAD_REQUEST)
        else:
            return JSONResponse(message, status_code=status.HTTP_404_NOT_FOUND)

    async def search(self, service: Optional[ServiceDefault] = None, name: Optional[str] = "", id: Optional[int] = -1,
                     free_fields: dict = {},
                     message: Optional[dict[str, str]] = None):

        db: Session = await get_db()

        if service is None:
            service = self.service

        if message is None:
            message = {"code": "Erro", "text": "Not found"}

        _item: dict | list

        try:
            if id >= 0:
                _item = await service.get(db, id, max_deep=MAX_DEEP)
            elif name:
                _item = await service.search(db, free_fields | {"name": name})
            elif free_fields:
                _item = await service.search(db, free_fields)
            else:
                _item = await service.get_all(db)
        except ServiceError:
            return JSONResponse(message, status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(_item, status_code=status.HTTP_200_OK)

    async def delete(self, service: Optional[ServiceDefault] = None, id: Optional[int] = -1,
                     message_sucess: dict[str, str] = None,
                     message_fail: Optional[dict[str, str]] = None):
        if service is None:
            service = self.service

        if message_sucess is None:
            message_sucess = {"code": "Ok", "text": f"Think with {id} deleted"}

        if message_fail is None:
            message_fail = {"code": "Erro", "text": f"Imposible to delete think with {id}"}

        _db: Session = await get_db()
        _deleted = await service.delete(_db, id)
        if _deleted:
            return JSONResponse(message_sucess, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(message_fail, status_code=status.HTTP_404_NOT_FOUND)


# inicializa
__startup__()
