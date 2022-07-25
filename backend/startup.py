from yaml import safe_load
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker

from typing import Callable

__database_url__: str = ''
__database_engine__: Engine = None

__SessionLocal__: Callable = None


# Dependency
def get_db():
    db = __SessionLocal__()
    try:
        yield db
    finally:
        db.close()


def __startup__() -> None:
    global __database_url__, __database_engine__, __SessionLocal__

    _FILE: str = 'config.yaml'
    _DATABASE_URL_ENV_NAME = 'DATABASE_URL'
    _DEBUG: bool = True

    yaml_confs = {}
    try:
        yaml_confs = safe_load(open(_FILE))
    except FileNotFoundError:
        yaml_confs = {"database": {}}

    drive = 'mariabd' if "drive" not in yaml_confs['database'] else yaml_confs['database']['drive']
    user = 'contas' if "user" not in yaml_confs['database'] else yaml_confs['database']['user']
    password = 'contas123' if "password" not in yaml_confs['database'] else yaml_confs['database']['password']
    url = 'localhost' if "url" not in yaml_confs['database'] else yaml_confs['database']['url']
    name = 'contabilidade' if "name" not in yaml_confs['database'] else yaml_confs['database']['name']
    __database_url__ = getenv(_DATABASE_URL_ENV_NAME, f'{drive}://{user}:{password}@{url}/{name}?charset=utf8')
    if drive == "sqlite":
        __database_engine__ = create_engine(__database_url__, echo=_DEBUG, future=True,
                                            connect_args={"check_same_thread": False})
    else:
        __database_engine__ = create_engine(__database_url__, echo=_DEBUG, future=True)

    __SessionLocal__ = sessionmaker(bind=__database_engine__, autocommit=False, autoflush=False)


__startup__()
