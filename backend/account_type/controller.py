from typing import Optional

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .data import AccountTypeData
from .service import AccountTypeService
from startup import get_db

templates = Jinja2Templates(directory='account_type/templates')
default = Jinja2Templates(directory='Templates')

app = FastAPI()

@app.put("/", response_class=JSONResponse)
@app.post("/", response_class=JSONResponse)
def new(request: Request, account_type: AccountTypeData | list[AccountTypeData], db: Session = Depends(get_db)):
    accounts_type: list[AccountTypeData] = []
    if isinstance(account_type, list):
        for data in account_type:
            accounts_type.append(AccountTypeService.save(db, data))
    else:
        accounts_type.append(AccountTypeService.save(db, account_type))
    return templates.TemplateResponse('fulldata.json', {"request": request, "accounts": accounts_type},
                                      headers={'content-type': 'application/json'})


@app.get("/", response_class=JSONResponse)
def search(request: Request, name: Optional[str] = "", db: Session = Depends(get_db)):
    return templates.TemplateResponse('fulldata.json', {"request": request,
                                                        "accounts": AccountTypeService.search(db, name)},
                                      headers={'content-type': 'application/json'})


@app.delete("/{id}", response_class=JSONResponse)
def delete(request: Request, id: int, db: Session = Depends(get_db)):
    if AccountTypeService.delete(db, id):
        return default.TemplateResponse('msg.json',
                                        {"request": request, "message": {"code": "ok", "text": "Account type deleted"}},
                                        headers={'content-type': 'application/json'})
    return default.TemplateResponse('msg.json',
                                    {"request": request, "message": {"code": "erro",
                                                                     "text": f"Error excluding account type id {id}"}},
                                   status_code=404, headers={'content-type': 'application/json'})
