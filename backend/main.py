from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.routing import Mount

from account.controller import app as account
from account_type.controller import app as account_type
from currency.controller import app as currency
from operation_type.controller import app as operation_type

app = FastAPI(routes=[Mount("/account", account),
                      Mount("/account-type", account_type),
                      Mount("/currency", currency),
                      Mount("/operation-type", operation_type)
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
