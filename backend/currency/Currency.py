from typing import Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy import Column, VARCHAR, BOOLEAN
from sqlalchemy.orm import relationship

from default import Mix, Base, \
    DataModelDefault, MessageDataDefault, \
    ControllerDefault as Controller, ServiceDefault


class Currency(Base, Mix):
    name = Column(VARCHAR(200), nullable=False)
    alias = Column(VARCHAR(5), nullable=False)
    default = Column(BOOLEAN, default=False)

    accounts = relationship("Account", back_populates="my_currency")


class CurrencyData(DataModelDefault):
    id: Optional[int]
    name: Optional[str]
    alias: Optional[str]
    default: Optional[bool]
    deleted: Optional[bool]


class Service(ServiceDefault):
    def __init__(self, database_class=Currency):
        super().__init__(database_class=database_class)

    def save(self, db, data: CurrencyData):
        if data.default and self.repository.search_by_fields(db, self.database_class, {"default": True}):
            return {"code": "Erro", "text": "It MUST have only one default currency"}, status.HTTP_400_BAD_REQUEST
        return super().save(db, data)


app: FastAPI = FastAPI()
__controller__: Controller = Controller(Service())


@app.get("/{id}", response_class=JSONResponse, response_model=CurrencyData)
@app.get("/", response_class=JSONResponse, response_model=list[CurrencyData])
async def search(name: Optional[str] = '', id: Optional[int] = -1, alias: Optional[str] = None,
                 default: Optional[bool] = None):
    return __controller__.search(name=name, id=id, free_fields={"alias": alias, "default": default})


@app.put("/", response_class=JSONResponse, response_model=list[CurrencyData])
@app.post("/", response_class=JSONResponse, response_model=list[CurrencyData], status_code=201)
async def create(account: CurrencyData | list[CurrencyData]):
    return __controller__.new(data=account)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return __controller__.delete(id=id, message_sucess={"code": "ok", "text": f"Currency with id {id} deleted"})
