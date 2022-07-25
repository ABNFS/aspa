from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from account.controller import app as account
from account_type.controller import app as account_type
from currency.controller import app as currency
from operation_type.controller import app as operation_type

app = FastAPI()
app.mount("/account", account)
app.mount("/account_type", account_type)
app.mount("/currency", currency)
app.mount("/operation_type", operation_type)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <body>
    It's working! Coming Soon.
    </body>
    </html>
    """
