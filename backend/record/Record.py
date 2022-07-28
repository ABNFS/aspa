from typing import Optional
from datetime import date

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import relationship, Session
from sqlalchemy import BIGINT, VARCHAR, DATE, Column, ForeignKey, Table

from default import ServiceDefault, ControllerDefault as Controller, \
    DataModelDefault, Mix, MessageDataDefault, Base

from account.Account import Account

tag_recorde = Table(
    "tag_record",
    Base.metadata,
    Column("record", ForeignKey("record.id"), primary_key=True),
    Column("tag", ForeignKey("tag.id"), primary_key=True)
)


class Record(Base, Mix):
    anotation = Column(VARCHAR(100), nullable=True)
    date = Column(DATE, nullable=False)
    amount = Column(BIGINT, nullable=False)
    account_debit = Column(BIGINT, ForeignKey(Account.id), nullable=False)
    account_credit = Column(BIGINT, ForeignKey(Account.id), nullable=False)
    my_tags = relationship('Tag', secondary=tag_recorde, back_populates='my_records')

    my_credit_accounts = relationship('Account', back_populates='records_with_credits', foreign_keys=[account_credit])
    my_debit_accounts = relationship('Account', back_populates='records_with_debits', foreign_keys=[account_debit])


class RecordData(DataModelDefault):
    from account.Account import AccountData
    anotation: Optional[str]
    date: Optional[date]
    amount: Optional[int]
    account_debit: Optional[int | AccountData]
    account_credit: Optional[int | AccountData]
    my_tags: Optional[list[int]]


class Service(ServiceDefault):

    def save(self, db: Session, data: RecordData):
        _my_tags: list[int] = data.my_tags
        _item, _status = super().save(db, data)
        if _status == status.HTTP_201_CREATED and "id" in _item:
            for tag in _my_tags:
                self.repository.raw_insert(db, tag_recorde, tag=tag, record=_item["id"])
        return _item, _status


app = FastAPI()
__controller__ = Controller(Service(database_class=Record))


@app.get("/{id}", response_class=JSONResponse, response_model=RecordData)
@app.get("/", response_class=JSONResponse, response_model=list[RecordData])
async def search(name: Optional[str] = '', id: Optional[int] = -1):
    return __controller__.search(name=name, id=id)


@app.put("/", response_class=JSONResponse, response_model=list[RecordData])
@app.post("/", response_class=JSONResponse, response_model=list[RecordData], status_code=201)
async def create(record: RecordData | list[RecordData]):
    return __controller__.new(data=record)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return __controller__.delete(id=id, message_sucess={"code": "Ok", "text": f"Record {id} was deleted."})
