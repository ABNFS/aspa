from typing import Optional, ClassVar

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from default import Mix, Base, DataModelDefault, MessageDataDefault, ControllerDefault, ServiceDefault
from sqlalchemy import Column, ForeignKey, VARCHAR, BIGINT, BOOLEAN
from sqlalchemy.orm import relationship, declared_attr, Session

from account_type import AccountType
from currency import Currency, CurrencyService


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
    my_records = relationship('AccountRecord', back_populates="account_in_record")


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


class AccountService(ServiceDefault):
    currency_service: CurrencyService

    def __init__(self):
        super().__init__(database_class=Account)
        self.currency_service = CurrencyService()

    async def can_operate(self, db: Session, id: int):
        account = await self.repository.__get_by_id__(db=db, cls=Account, id=id)
        return account.operate if account else False

    async def save(self, db: Session, data: AccountData, max_deep: int = -1) -> dict:
        if not data.currency:
            _default_currency = await self.currency_service.get_default(db)
            data.currency = _default_currency.id
        if max_deep >= 0:
            return await super().save(db, data, max_deep)
        return await super().save(db, data)

    async def new(self, db: Session, data: AccountData, max_deep: int = -1) -> dict:
        if not data.currency:
            _default_currency = await self.currency_service.get_default(db)
            data.currency = _default_currency.id
        if max_deep >= 0:
            return await super().new(db, data, max_deep)
        return await super().new(db, data)


class AccountController(ControllerDefault):
    def __init__(self):
        super().__init__(AccountService())


app: FastAPI = FastAPI()


@app.get("/{id}", response_class=JSONResponse, response_model=AccountData)
@app.get("/", response_class=JSONResponse, response_model=list[AccountData])
async def search(name: Optional[str] = '', id: Optional[int] = -1, code: Optional[str] = None):
    return await AccountController().search(name=name, id=id, free_fields={"code": code})


@app.put("/", response_class=JSONResponse, response_model=list[AccountData])
@app.post("/", response_class=JSONResponse, response_model=list[AccountData], status_code=201)
async def create(account: AccountData | list[AccountData]):
    return await AccountController().new(data=account)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return await AccountController().delete(id=id,
                                            message_sucess={"code": "ok", "text": f"Account with id {id} deleted"})
