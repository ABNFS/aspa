from typing import Optional

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session


from .data import CurrencyData
from .service import CurrencyService

from startup import get_db

templates = Jinja2Templates(directory="currency/templates")

app = FastAPI()


@app.get("/", response_class=JSONResponse)
async def search(request: Request, name: Optional[str] = '', db: Session = Depends(get_db)):
    return templates.TemplateResponse("fulldata.json", {"request": request,
                                                        "currencys": CurrencyService.search(db, name)},
                                      headers={'content-type': 'application/json'})


@app.post("/", response_class=JSONResponse)
async def create(request: Request, currency: CurrencyData | list[CurrencyData], db: Session = Depends(get_db)):
    currencys: list[CurrencyData] = []
    if isinstance(currency, list):
        for data in currency:
            currencys.append(CurrencyService.new(db, data))
    else:
        currencys.append(CurrencyService.new(db, currency))
    return templates.TemplateResponse("fulldata.json",
                                      {"request": request, "currencys": currencys},
                                      headers={'content-type': 'application/json'})


@app.put("/")
async def update(name: str, db: Session = Depends(get_db)):
    return {"message": f"Hello {name}"}


@app.put("/")
async def delete(name: str, db: Session = Depends(get_db)):
    return {"message": f"Hello {name}"}
