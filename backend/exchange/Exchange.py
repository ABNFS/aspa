from typing import Optional
from datetime import datetime

from pydantic import ValidationError
from sqlalchemy import Column, BIGINT, DATETIME, ForeignKey

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from currency import CurrencyService, Currency
from default import ControllerDefault, ServiceDefault, \
    Base, Mix, MessageDataDefault, DataModelDefault
from default import log, ServiceError


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
    service_currency: CurrencyService

    def __init__(self):
        super().__init__(database_class=Exchange)
        self.service_currency = CurrencyService()

    async def __convert_exchange_data(self, db, data: ExchangeDataOut) -> ExchangeData:
        currency_default: Currency = await self.service_currency.get_default(db)
        try:
            if currency_default:
                return ExchangeData(data, currency_default.id)
            else:
                raise ServiceError("No default Currency found!")
        except ValidationError:
            log.debug(f'Erro in Exchange {data}')
            raise ServiceError(message='Erro in Exchange')

    async def new(self, db, data: ExchangeDataOut, max_deep: int = -1) -> dict:
        if max_deep == -1:
            return await super().new(db, await self.__convert_exchange_data(db,data))
        return await super().new(db, await self.__convert_exchange_data(db,data), max_deep)

    async def save(self, db, data: ExchangeDataOut, max_deep: int = -1) -> dict:
        if max_deep == -1:
            return await super().save(db, await self.__convert_exchange_data(db, data))
        return await super().save(db, await self.__convert_exchange_data(db, data), max_deep)


class Controller(ControllerDefault):

    async def search(self, id: Optional[int] = -1, startdate: Optional[datetime] = None, enddate: Optional[datetime] = None,
               currency: Optional[int] = -1):
        _when: dict = {}
        _currency: dict = {}

        if (not enddate) and startdate:  # TODO: Use TimeZone here.
            enddate = datetime.now()

        if startdate and enddate:
            _when = {"when": [startdate, enddate]}

        if currency >= 0:
            _currency = {"currency_buy": currency}

        return await super().search(service=self.service, name=None, id=id, free_fields=_when | _currency)


app = FastAPI()


@app.get("/{id}", response_class=JSONResponse, response_model=ExchangeDataOut)
@app.get("/", response_class=JSONResponse, response_model=list[ExchangeDataOut])
async def search(id: Optional[int] = -1, datainicio: Optional[datetime] = None, datafim: Optional[datetime] = None,
                 currency: Optional[int] = -1):
    return await Controller(Service()).search(id, datainicio, datafim, currency)


@app.put("/", response_class=JSONResponse, response_model=list[ExchangeDataOut])
@app.post("/", response_class=JSONResponse, response_model=list[ExchangeDataOut], status_code=201)
async def create(exchange: ExchangeDataOut | list[ExchangeDataOut]):
    return await Controller(Service()).new(data=exchange)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return await Controller(Service()).delete(id=id, message_sucess={"code": "ok", "text": f"Account with id {id} deleted"})
