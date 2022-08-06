from typing import Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy import Column, VARCHAR, BOOLEAN
from sqlalchemy.orm import relationship

from default import Mix, Base, DEFAULT_DEEP, \
    DataModelDefault, MessageDataDefault, \
    ControllerDefault as Controller, ServiceDefault


class Currency(Base, Mix):
    name = Column(VARCHAR(200), nullable=False)
    iso_code = Column(VARCHAR(5), nullable=False)
    default = Column(BOOLEAN, default=False)

    accounts = relationship("Account", back_populates="my_currency")


class CurrencyData(DataModelDefault):
    id: Optional[int]
    name: Optional[str]
    iso_code: Optional[str]
    default: Optional[bool]
    deleted: Optional[bool]


class Service(ServiceDefault):
    def __init__(self, database_class=Currency):
        super().__init__(database_class=database_class)

    async def save(self, db, data: CurrencyData, max_deep: int = DEFAULT_DEEP):
        have_default_currency = await self.repository.search_by_fields(db, self.database_class, {"default": True})
        if data.default and have_default_currency:
            return {"code": "Erro", "text": "It MUST have only one default currency"}, status.HTTP_400_BAD_REQUEST
        return await super().save(db, data, max_deep)


app: FastAPI = FastAPI()


@app.get("/{id}", response_class=JSONResponse, response_model=CurrencyData)
@app.get("/", response_class=JSONResponse, response_model=list[CurrencyData])
async def search(name: Optional[str] = '', id: Optional[int] = -1, alias: Optional[str] = None,
                 default: Optional[bool] = None):
    return await Controller(Service()).search(name=name, id=id, free_fields={"alias": alias, "default": default})


@app.put("/", response_class=JSONResponse, response_model=list[CurrencyData])
@app.post("/", response_class=JSONResponse, response_model=list[CurrencyData], status_code=201)
async def create(account: CurrencyData | list[CurrencyData]):
    return await Controller(Service()).new(data=account)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return await Controller(Service()).delete(id=id, message_sucess={"code": "ok", "text": f"Currency with id {id} deleted"})
