from yaml import load, Loader
from os import getenv

_FILE: str = 'config.yaml'
_DATABASE_URL_ENV_NAME = 'DATABASE_URL'
database_url: str = ''


def __startup__() -> None:
    global database_url
    yaml_confs = {}
    try:
        yaml_confs = load(open(_FILE), Loader=Loader)
    except FileNotFoundError:
        yaml_confs = {"database": {}}

    drive = 'mariabd' if "drive" not in yaml_confs['database'] else yaml_confs['database']['drive']
    user = 'contas' if "user" not in yaml_confs['database'] else yaml_confs['database']['user']
    password = 'contas123' if "password" not in yaml_confs['database'] else yaml_confs['database']['password']
    url = 'localhost' if "url" not in yaml_confs['database'] else yaml_confs['database']['url']
    name = 'contabilidade' if "name" not in yaml_confs['database'] else yaml_confs['database']['name']
    database_url = getenv(_DATABASE_URL_ENV_NAME, f'{drive}://{user}:{password}@{url}/{name}?charset=utf8')


__startup__()
