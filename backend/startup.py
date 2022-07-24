from yaml import safe_load
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.future import Engine

database_url: str = ''
database_engine: Engine = None


def __startup__() -> None:
    global database_url, database_engine

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
    database_url = getenv(_DATABASE_URL_ENV_NAME, f'{drive}://{user}:{password}@{url}/{name}?charset=utf8')
    if drive == "sqlite":
        database_engine = create_engine(database_url, echo=_DEBUG, future=True,
                                        connect_args={"check_same_thread": False})
    else:
        database_engine = create_engine(database_url, echo=_DEBUG, future=True)


__startup__()
