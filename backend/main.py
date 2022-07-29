from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.routing import Mount

from account import app as account_app
from account_type import app as account_type
from currency import app as currency_app
from exchange import app as exchange_app
from operation_type import app as operation_app
from record import app as record_app
from tag import app as tag_app

app = FastAPI(routes=[Mount("/account", account_app),
                      Mount("/account-type", account_type),
                      Mount("/currency", currency_app),
                      Mount("/exchange", exchange_app),
                      Mount("/operation-type", operation_app),
                      Mount("/record", record_app),
                      Mount("/tag", tag_app)
                      ])


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <body>
    It's working!
    </body>
    </html>
    """
