from fastapi import FastAPI
from fastapi.responses import HTMLResponse


from conta.controller import app as conta
from dinheiro.controller import app as dinheiro

app = FastAPI()
app.mount("/conta", conta)
app.mount("/dinheiro", dinheiro)



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
