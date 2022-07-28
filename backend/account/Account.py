from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse


from default import Mix, Base, \
    DataModelDefault, MessageDataDefault, \
    ControllerDefault as Controller, ServiceDefault as Service
from sqlalchemy import Column, ForeignKey, VARCHAR, BIGINT, BOOLEAN
from sqlalchemy.orm import relationship, declared_attr


class Account(Mix, Base):
    from account_type.AccountType import AccountType
    from currency.Currency import Currency

    code = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(200), nullable=False)
    balance = Column(BIGINT, nullable=True, default=0)
    alias = Column(VARCHAR(5), nullable=True, default=None)
    currency = Column(BIGINT, ForeignKey(Currency.id), nullable=True, default=1)
    account_type = Column(BIGINT, ForeignKey(AccountType.id), nullable=False)
    operate = Column(BOOLEAN, nullable=False, default=False)

    @declared_attr
    def parent(cls):
        return Column(BIGINT, ForeignKey(cls.id), nullable=True, default=None)

    @declared_attr
    def children(cls):
        return relationship(cls)

    my_account_type = relationship("AccountType", back_populates="accounts")
    my_currency = relationship("Currency", back_populates="accounts")
    records_with_credits = relationship('Record', back_populates="my_credit_accounts",
                                       foreign_keys="Record.account_credit")
    records_with_debits = relationship('Record', back_populates="my_debit_accounts",
                                       foreign_keys="Record.account_debit")


class AccountData(DataModelDefault):
    id: Optional[int]
    code: Optional[str]
    name: Optional[str]
    balance: Optional[int]
    alias: Optional[str]
    currency: Optional[int]
    account_type: Optional[int]
    parent: Optional[int]
    operate: Optional[bool]
    deleted: Optional[bool]

app: FastAPI = FastAPI()
__controller__: Controller = Controller(Service(database_class=Account))


@app.get("/{id}", response_class=JSONResponse, response_model=AccountData)
@app.get("/", response_class=JSONResponse, response_model=list[AccountData])
async def search(name: Optional[str] = '', id: Optional[int] = -1, code: Optional[str] = None):
    return __controller__.search(name=name, id=id, free_fields={"code": code})


@app.put("/", response_class=JSONResponse, response_model=list[AccountData])
@app.post("/", response_class=JSONResponse, response_model=list[AccountData], status_code=201)
async def create(account: AccountData | list[AccountData]):
    return __controller__.new(data=account)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return __controller__.delete(id=id, message_sucess={"code": "ok", "text": f"Account with id {id} deleted"})
