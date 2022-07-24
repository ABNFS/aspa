from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from .service import DinheiroService

templates = Jinja2Templates(directory="dinheiro/templates")

app = FastAPI()


@app.get("/", response_class=JSONResponse)
async def listar(request: Request, nome: str = ''):
    return templates.TemplateResponse("completo.json", {"request": request, "dinheiros": DinheiroService.busca(nome)})


@app.post("/")
async def criar(name: str):
    return {"message": f"Hello {name}"}


@app.put("/")
async def atualizar(name: str):
    return {"message": f"Hello {name}"}


@app.put("/")
async def apagar(name: str):
    return {"message": f"Hello {name}"}
