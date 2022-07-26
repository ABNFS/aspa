from typing import Optional
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .service import AccountService
from .data import AccountData

from startup import get_db

templates = Jinja2Templates(directory="account/templates")
default_templates = Jinja2Templates(directory="Templates")

app = FastAPI()


@app.get("/", response_class=JSONResponse)
async def search(request: Request, name: Optional[str] = '', db: Session = Depends(get_db)):
    return templates.TemplateResponse("fulldata.json", {"request": request,
                                                        "accounts": AccountService.search(db, name)},
                                      headers={'content-type': 'application/json'})


@app.put("/", response_class=JSONResponse)
@app.post("/", response_class=JSONResponse)
async def create(request: Request, account: AccountData | list[AccountData], db: Session = Depends(get_db)):
    accounts: list[AccountData] = []

    if isinstance(account, list):
        for data in account:
            accounts.append(AccountService.save(db, data))
    else:
        accounts.append(AccountService.save(db, account))
    return templates.TemplateResponse("fulldata.json", {"request": request, "accounts": accounts},
                                      headers={'content-type': 'application/json'})


@app.delete("/{id}")
async def delete(request: Request, id: int, db: Session = Depends(get_db)):
    if AccountService.delete(db, id):
        return default_templates.TemplateResponse('msg.json', {"request": request,
                                                               "message": {"code": "ok",
                                                                           "text": f"Account {id} deleted."}},
                                                  headers={'content-type': 'application/json'})
    return default_templates.TemplateResponse('msg.json', {"request": request,
                                                           "message": {"code": "Error",
                                                                       "text": f"Cannot delete the account."}},
                                              headers={'content-type': 'application/json'})
