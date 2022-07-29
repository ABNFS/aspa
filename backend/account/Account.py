from typing import Optional, ClassVar

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from default import Mix, Base, \
    DataModelDefault, MessageDataDefault, \
    ControllerDefault as Controller, ServiceDefault
from sqlalchemy import Column, ForeignKey, VARCHAR, BIGINT, BOOLEAN
from sqlalchemy.orm import relationship, declared_attr, Session

from account_type.AccountType import AccountType
from currency.Currency import Currency
from record.Record import account_record


class Account(Mix, Base):
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
    my_records = relationship('Record', back_populates="my_accounts", secondary=account_record)

    def __str__(self):
        return f'{self.code} - {self.name}{f" ({self.alias})" if self.alias else None} - {str(self.account_type)}'


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


class Service(ServiceDefault):

    def __init__(self, database_class: ClassVar = Account):
        super().__init__(database_class=database_class)

    def can_operate(self, db: Session, id: int):
        account = self.repository.__get_by_id__(db=db, cls=Account,id=id)
        return account.operate if account else False


app: FastAPI = FastAPI()


@app.get("/{id}", response_class=JSONResponse, response_model=AccountData)
@app.get("/", response_class=JSONResponse, response_model=list[AccountData])
async def search(name: Optional[str] = '', id: Optional[int] = -1, code: Optional[str] = None):
    return Controller(Service()).search(name=name, id=id, free_fields={"code": code})


@app.put("/", response_class=JSONResponse, response_model=list[AccountData])
@app.post("/", response_class=JSONResponse, response_model=list[AccountData], status_code=201)
async def create(account: AccountData | list[AccountData]):
    return Controller(Service()).new(data=account)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return Controller(Service()).delete(id=id, message_sucess={"code": "ok", "text": f"Account with id {id} deleted"})
