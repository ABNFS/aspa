from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="conta/templates")

app = FastAPI()

@app.get("/", response_class=JSONResponse)
async def listar(request: Request):
    contas : list = [
        {"codigo": 123, "sigla": "CC", "nome": "conta-corrente", "saldo": 23, "tipoSaldo": {"nome": "credito"}, "tipoConta": {"nome": "ativo"}, "moeda": {"nome": "Reais"} },
        {"codigo": "abc", "sigla": "CT", "nome": "cartão", "saldo": 123, "tipoSaldo": {"nome": "debito"}, "tipoConta": {"nome": "exegível"}, "moeda": {"nome": "Reais"} }
    ]
    return templates.TemplateResponse("completo.json", {"request": request, "contas": contas})

@app.post("/")
async def criar(name: str):
    return {"message": f"Hello {name}"}

@app.put("/")
async def atualizar(name: str):
    return {"message": f"Hello {name}"}

@app.put("/")
async def apagar(name: str):
    return {"message": f"Hello {name}"}
