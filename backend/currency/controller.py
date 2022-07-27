from typing import Optional

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .data import CurrencyData
from .service import CurrencyService

from startup import get_db
from Data import DefaultMessageData

templates = Jinja2Templates(directory="currency/templates")
default_templates = Jinja2Templates(directory="Templates")

app = FastAPI()


@app.get("/{id}", response_class=JSONResponse, response_model=CurrencyData)
@app.get("/", response_class=JSONResponse, response_model=list[CurrencyData])
async def search(request: Request, name: Optional[str] = '', id: Optional[int] = -1, db: Session = Depends(get_db)):
    if id >= 0:
        currency = CurrencyService.get(db, id)
        if currency:
            return templates.TemplateResponse("one.json", {"request": request, "currency": currency},
                                              headers={'content-type': 'application/json'})
        return default_templates.TemplateResponse("msg.json", {"request": request,
                                                               "messagem": {"code": "Erro",
                                                                            "text": "Currency not found"}},
                                                  headers={"content-type": "application/json"},
                                                  status_code=404)
    return templates.TemplateResponse("fulldata.json", {"request": request,
                                                        "currencys": CurrencyService.search(db, name)},
                                      headers={'content-type': 'application/json'})


@app.put("/", response_class=JSONResponse, response_model=list[CurrencyData])
@app.post("/", response_class=JSONResponse, response_model=list[CurrencyData], status_code=201)
async def create(request: Request, currency: CurrencyData | list[CurrencyData], db: Session = Depends(get_db)):
    currencys: list[CurrencyData] = []
    if isinstance(currency, list):
        for data in currency:
            currencys.append(CurrencyService.save(db, data))
    else:
        currencys.append(CurrencyService.save(db, currency))
    return templates.TemplateResponse("fulldata.json",
                                      {"request": request, "currencys": currencys},
                                      headers={'content-type': 'application/json'},
                                      status_code=201 if request.method == 'POST' else 200
                                      )


@app.delete("/{id}", response_class=JSONResponse, response_model=DefaultMessageData)
async def delete(request: Request, id: int, db: Session = Depends(get_db)):
    if CurrencyService.delete(db, id):
        return default_templates.TemplateResponse('msg.json', {'request': request, 'message':
            {'code': 'ok', 'text': f'The currency with {id} was deleted.'}},
                                                  headers={'content-type': 'aplication/json'})
    return default_templates.TemplateResponse('msg.json', {'request': request,
                                                           'message': {'code': 'Erro',
                                                                       'text': f'Impossible delete the currency {id}'}},
                                                  headers={'content-type': 'aplication/json'},
                                              status_code=404)
