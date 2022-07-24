from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from account.controller import app as conta
from currency.controller import app as dinheiro

app = FastAPI()
app.mount("account", conta)
app.mount("currency", dinheiro)

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
