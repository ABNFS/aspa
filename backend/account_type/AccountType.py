from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from default import Mix, Base, \
    DataModelDefault, MessageDataDefault, \
    ControllerDefault as Controller, ServiceDefault as Service
from sqlalchemy import Column, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship


class AccountType(Base, Mix):
    from operation_type.Operation import OperationType
    __tablename__ = 'account_type'

    name = Column(VARCHAR(26), nullable=False, unique=True)
    alias = Column(VARCHAR(3), nullable=False, unique=True)
    operation = Column(ForeignKey(OperationType.id), nullable=False)

    my_operation = relationship("OperationType", back_populates="accounts_type")
    accounts = relationship("Account", back_populates="my_account_type")



class AccountTypeData(DataModelDefault):
    id: Optional[int]
    name: Optional[str]
    alias: Optional[str]
    operation: Optional[int]
    deleted: Optional[bool]


app = FastAPI()
__controller__ = Controller(Service(database_class=AccountType))


@app.get("/{id}", response_class=JSONResponse, response_model=AccountTypeData)
@app.get("/", response_class=JSONResponse, response_model=list[AccountTypeData])
async def search(name: Optional[str] = '', id: Optional[int] = -1):
    return await __controller__.search(name=name, id=id)

@app.put("/", response_class=JSONResponse, response_model=list[AccountTypeData])
@app.post("/", response_class=JSONResponse, response_model=list[AccountTypeData], status_code=201)
async def create(account_type: AccountTypeData | list[AccountTypeData]):
    return await __controller__.new(data=account_type)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return await __controller__.delete(id=id, message_sucess={
        "code": "ok", "text": f"Account Type with id {id} deleted"})
