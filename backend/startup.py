from pathlib import Path

from yaml import safe_load
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker

from typing import Callable, Optional, Any

_DATABASE_URL_ENV_NAME = 'DATABASE_URL'
_ALLOW_ORIGINS_ENV_NAME = 'CORS_ALLOW_ORIGIN'
_CONFIG_FILE_ENV_NAME = 'CONFIG_FILE_PATH'
_FILE: str = './config.yaml'
_DEBUG: bool = True

__database_url__: str = ''
__database_engine__: Engine = None

SessionLocal: Callable = None

origins: list = []


def __startup__(path: Optional[Path] = None) -> None:
    def get_config_file_from_env() -> Path:
        return Path(getenv(_CONFIG_FILE_ENV_NAME, _FILE))

    def get_yaml_dict(path_to_file: Optional[Path] = None) -> dict[str:Any]:
        yaml_confs: dict[str:Any]
        if path_to_file is None:
            path_to_file = get_config_file_from_env()
        try:
            yaml_confs = safe_load(open(path_to_file))
        except FileNotFoundError:
            yaml_confs = {'database': {}}
        return yaml_confs

    def make_url_db_from_config_file(path_to_file: Optional[Path] = None) -> str:
        yaml_confs = get_yaml_dict(path_to_file)
        _drive = 'mariabd' if "drive" not in yaml_confs['database'] else yaml_confs['database']['drive']
        _user = 'contas' if "user" not in yaml_confs['database'] else yaml_confs['database']['user']
        _password = 'contas123' if "password" not in yaml_confs['database'] else yaml_confs['database']['password']
        _url = 'localhost' if "url" not in yaml_confs['database'] else yaml_confs['database']['url']
        _name = 'contabilidade' if "name" not in yaml_confs['database'] else yaml_confs['database']['name']

        return f'{_drive}://{_user}:{_password}@{_url}/{_name}?charset=utf8'

    def make_origins_from_config_file(path_to_file: Optional[Path] = None) -> list:
        config = get_yaml_dict(path_to_file)
        allow_origins_file: list = [] if "allow_origins" not in config else config["allow_origins"]
        allow_origins_env: str = getenv(_ALLOW_ORIGINS_ENV_NAME, None)
        return allow_origins_env.split(" ") if allow_origins_env else allow_origins_file

    global __database_url__, __database_engine__, SessionLocal, origins

    __database_url__ = getenv(_DATABASE_URL_ENV_NAME, make_url_db_from_config_file(path))
    __drive = __database_url__.split(':')[0]
    if __drive == "sqlite":
        __database_engine__ = create_engine(__database_url__, echo=_DEBUG, future=True,
                                            connect_args={"check_same_thread": False})
    else:
        __database_engine__ = create_engine(__database_url__, echo=_DEBUG, future=True)

    SessionLocal = sessionmaker(bind=__database_engine__, autocommit=False, autoflush=False, expire_on_commit=True)
    origins = make_origins_from_config_file()


__startup__()
