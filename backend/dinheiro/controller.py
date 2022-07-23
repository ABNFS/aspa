from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="dinheiro/templates")

app = FastAPI()

@app.get("/", response_class=JSONResponse)
async def listar(request: Request):
    dinheiros : list = [
        {"id": 1, "nome": "Real", "sigla": "R$", "taxaCambio": 100},
        {"id": 2, "nome": "Dólar", "sigla": "US$", "taxaCambio": 469}
    ]
    return templates.TemplateResponse("completo.json", {"request": request, "dinheiros": dinheiros})

@app.post("/")
async def criar(name: str):
    return {"message": f"Hello {name}"}

@app.put("/")
async def atualizar(name: str):
    return {"message": f"Hello {name}"}

@app.put("/")
async def apagar(name: str):
    return {"message": f"Hello {name}"}
