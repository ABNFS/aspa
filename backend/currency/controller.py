from typing import Optional

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .data import CurrencyData
from .service import CurrencyService

from startup import get_db

templates = Jinja2Templates(directory="currency/templates")
default_templates = Jinja2Templates(directory="Templates")

app = FastAPI()


@app.get("/", response_class=JSONResponse)
async def search(request: Request, name: Optional[str] = '', db: Session = Depends(get_db)):
    return templates.TemplateResponse("fulldata.json", {"request": request,
                                                        "currencys": CurrencyService.search(db, name)},
                                      headers={'content-type': 'application/json'})


@app.put("/", response_class=JSONResponse, status_code=200)
@app.post("/", response_class=JSONResponse, status_code=201)
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


@app.delete("/{id}")
async def delete(request: Request, id: int, db: Session = Depends(get_db)):
    if CurrencyService.delete(db, id):
        return default_templates.TemplateResponse('msg.json', {'request': request, 'message':
            {'code': 'ok', 'text': f'The currency with {id} was deleted.'}},
                                                  headers={'content-type': 'aplication/json'})
    return default_templates.TemplateResponse('msg.json', {'request': request, 'message':
            {'code': 'Error', 'text': f'Impossible to delete the currency with {id}.'}},
                                                  headers={'content-type': 'aplication/json'}, status_code=404)
