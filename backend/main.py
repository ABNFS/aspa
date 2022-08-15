from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.routing import Mount
from fastapi.middleware.cors import CORSMiddleware

from account import app as account_app
from account_type import app as account_type
from currency import app as currency_app
from exchange import app as exchange_app
from operation_type import app as operation_app
from record import app as record_app
from tag import app as tag_app
from default import get_from_conf

_DEFAULT_DIGITS: int = 2
_ALLOW_ORIGINS_ENV_NAME = 'CORS_ALLOW_ORIGIN'

digits: int = get_from_conf(section='number', key='digits', default_value=_DEFAULT_DIGITS)


def __make_origins_from_config_file() -> list:
    from os import getenv
    allow_origins_from_file: list = get_from_conf('allow_origins', default_value=[])
    allow_origins_env: str = getenv(_ALLOW_ORIGINS_ENV_NAME, None)
    return allow_origins_env.split(" ") if allow_origins_env else allow_origins_from_file


app = FastAPI(routes=[Mount("/account", account_app),
                      Mount("/account-type", account_type),
                      Mount("/currency", currency_app),
                      Mount("/exchange", exchange_app),
                      Mount("/operation-type", operation_app),
                      Mount("/record", record_app),
                      Mount("/tag", tag_app)
                      ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=__make_origins_from_config_file(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <body>
    It's working!
    </body>
    </html>
    """


@app.get("/digits")
async def digits_to_show():
    return digits
