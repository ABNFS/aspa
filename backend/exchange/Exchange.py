from typing import Optional, ClassVar
from datetime import datetime

from pydantic import ValidationError
from sqlalchemy import Column, BIGINT, DATETIME, ForeignKey

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from default import ControllerDefault, ServiceDefault, \
    Base, Mix, MessageDataDefault, DataModelDefault


class Exchange(Base, Mix):
    currency_default = Column("currency_default", BIGINT, ForeignKey("currency.id"), default=1)
    currency_buy = Column("currency_buy", BIGINT, ForeignKey("currency.id"), nullable=False)
    when = Column("when", DATETIME, nullable=False)
    rate = Column("rate", BIGINT, nullable=False)


class ExchangeDataOut(DataModelDefault):
    currency: Optional[int]
    rate: Optional[int]
    when: Optional[datetime]


class ExchangeData(DataModelDefault):
    currency_default: int
    currency_buy: int
    rate: int
    when: datetime

    def __init__(self, out_model: ExchangeDataOut, default: int):
        super().__init__(currency_default=default, currency_buy=out_model.currency,
                         rate=out_model.rate, when=out_model.when)


class Service(ServiceDefault):

    def __init__(self):
        super().__init__(database_class=Exchange)

    def save(self, db, data: ExchangeDataOut):
        from currency.Currency import Currency
        currency_default: Currency = self.repository.search_by_fields(db, Currency, {"default": True})[0]
        new_data: ExchangeData | None
        try:
            new_data = ExchangeData(data, currency_default.id)
        except ValidationError:
            new_data = None
        return super().save(db, new_data)


class Controller(ControllerDefault):

    def search(self, id: Optional[int] = -1, startdate: Optional[datetime] = None, enddate: Optional[datetime] = None,
               currency: Optional[int] = -1):
        _when: dict = {}
        _currency: dict = {}

        if (not enddate) and startdate:  # TODO: Use TimeZone here.
            enddate = datetime.now()

        if startdate and enddate:
            _when = {"when": [startdate, enddate]}

        if currency >= 0:
            _currency = {"currency_buy": currency}

        return super().search(service=self.service, name=None, id=id, free_fields=_when | _currency)


app = FastAPI()


@app.get("/{id}", response_class=JSONResponse, response_model=ExchangeDataOut)
@app.get("/", response_class=JSONResponse, response_model=list[ExchangeDataOut])
async def search(id: Optional[int] = -1, datainicio: Optional[datetime] = None, datafim: Optional[datetime] = None,
                 currency: Optional[int] = -1):
    return Controller(Service()).search(id, datainicio, datafim, currency)


@app.put("/", response_class=JSONResponse, response_model=list[ExchangeDataOut])
@app.post("/", response_class=JSONResponse, response_model=list[ExchangeDataOut], status_code=201)
async def create(exchange: ExchangeDataOut | list[ExchangeDataOut]):
    return Controller(Service()).new(data=exchange)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return Controller(Service()).delete(id=id, message_sucess={"code": "ok", "text": f"Account with id {id} deleted"})
