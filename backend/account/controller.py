from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from .service import AcconutService

templates = Jinja2Templates(directory="account/templates")

app = FastAPI()

@app.get("/", response_class=JSONResponse)
async def list(request: Request, name: str = ""):
    return templates.TemplateResponse("fulldata.json", {"request": request, "accounts": AcconutService.search(name)})

@app.post("/")
async def create(name: str):
    return {"message": f"Hello {name}"}

@app.put("/")
async def update(name: str):
    return {"message": f"Hello {name}"}

@app.put("/")
async def delete(name: str):
    return {"message": f"Hello {name}"}
