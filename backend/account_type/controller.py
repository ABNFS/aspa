from typing import Optional

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .data import AccountTypeData
from .service import AccountTypeService
from startup import get_db

templates = Jinja2Templates(directory='account_type/templates')

app = FastAPI()


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
