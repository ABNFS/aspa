from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from default import Mix, Base, \
    DataModelDefault, MessageDataDefault, \
    ControllerDefault as Controller, ServiceDefault as Service
from sqlalchemy import Column, VARCHAR, CHAR
from sqlalchemy.orm import relationship


class OperationType(Base, Mix):
    __tablename__ = 'operation_type'

    name = Column(VARCHAR(20), nullable=False, unique=True)
    alias = Column(CHAR(1), nullable=False, unique=True)

    accounts_type = relationship("AccountType", back_populates="my_operation")
    my_records = relationship('AccountRecord', back_populates="account_in_record_operation_type")


class OperationTypeData(DataModelDefault):
    id: Optional[int]
    name: Optional[str]
    alias: Optional[str]


app: FastAPI = FastAPI()
__controller__: Controller = Controller(Service(database_class=OperationType))


@app.put("/", response_class=JSONResponse, status_code=200, response_model=list[OperationTypeData])
@app.post("/", response_class=JSONResponse, status_code=201, response_model=list[OperationTypeData])
async def new(operation_type: OperationTypeData | list[OperationTypeData]):
    return await __controller__.new(data=operation_type)


@app.get("/{id}", response_class=JSONResponse, response_model=OperationTypeData)
@app.get("/", response_class=JSONResponse, response_model=list[OperationTypeData])
async def search(name: Optional[str] = "", id: Optional[int] = -1):
    return await __controller__.search(name=name, id=id)


@app.delete("/{id}", response_class=JSONResponse, response_model=MessageDataDefault)
async def delete(id: int):
    return await __controller__.delete(id=id, message_sucess={"code": "Ok", "text": f"The Operation {id} was deleted."})
