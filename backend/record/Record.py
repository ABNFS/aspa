from typing import Optional
from datetime import date

from fastapi import FastAPI
from  fastapi.responses import JSONResponse

from sqlalchemy.orm import relationship
from sqlalchemy import BIGINT, VARCHAR, DATE, Column, ForeignKey, Table

from default import ServiceDefault as Service, ControllerDefault as Controller, \
    DataModelDefault, Mix, MessageDataDefault, Base

from account.Account import Account


tag_recorde = Table(
    "tag_record",
    Base.metadata,
    Column("record", ForeignKey("Record.id"), primary_key=True),
    Column("tag", ForeignKey("Tag.id"), primary_key=True)
)

class Record(Base, Mix):

    anotation = Column(VARCHAR(100), nullable=True)
    date = Column(DATE, nullable=False)
    amount = Column(BIGINT, nullable=False)
    account_debit = Column(BIGINT, ForeignKey(Account.id), nullable=False)
    account_credit = Column(BIGINT, ForeignKey(Account.id), nullable=False)
    # my_tags = relationship('Tag', secondary=tag_recorde, back_populates='my_records')

    my_credit_accounts = relationship('Account', back_populates='records_with_credits', foreign_keys=[account_credit])
    my_debit_accounts = relationship('Account', back_populates='records_with_debits', foreign_keys=[account_debit])


class RecordData(DataModelDefault):
    from account.Account import AccountData
    anotation: Optional[str]
    data: Optional[date]
    amount: Optional[int]
    account_debit: Optional[int | AccountData]
    account_credit: Optional[int | AccountData]


app = FastAPI()
__controller__ = Controller(Service(database_class=Record))

@app.get("/{id}", response_class=JSONResponse, response_model=RecordData)
@app.get("/", response_class=JSONResponse, response_model=list[RecordData])
async def search(name: Optional[str] = '', id: Optional[int] = -1):
    return __controller__.search(name=name, id=id)


@app.put("/", response_class=JSONResponse, response_model=list[RecordData])
@app.post("/", response_class=JSONResponse, response_model=list[RecordData], status_code=201)
async def create(account: RecordData | list[RecordData]):
    return __controller__.new(data=account)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return __controller__.delete(id=id, message_sucess={"code": "Ok", "text": f"Record {id} was deleted."})
