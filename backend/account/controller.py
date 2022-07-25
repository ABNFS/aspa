from typing import Optional
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .service import AccountService
from .data import AccountData

from startup import get_db

templates = Jinja2Templates(directory="account/templates")

app = FastAPI()


@app.get("/", response_class=JSONResponse)
async def search(request: Request, name: Optional[str] = '', db: Session = Depends(get_db)):
    return templates.TemplateResponse("fulldata.json", {"request": request,
                                                        "accounts": AccountService.search(db, name)},
                                      headers={'content-type': 'application/json'})


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


@app.put("/")
async def update(name: str, db: Session = Depends(get_db)):
    return {"message": f"Hello {name}"}


@app.put("/")
async def delete(name: str, db: Session = Depends(get_db)):
    return {"message": f"Hello {name}"}
