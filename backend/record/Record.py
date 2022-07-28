from typing import Optional
from datetime import date

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import relationship, Session
from sqlalchemy import BIGINT, VARCHAR, DATE, Column, ForeignKey, Table

from default import ServiceDefault, ControllerDefault as Controller, \
    DataModelDefault, Mix, MessageDataDefault, Base

tag_recorde = Table(
    "tag_record",
    Base.metadata,
    Column("record", ForeignKey("record.id"), primary_key=True),
    Column("tag", ForeignKey("tag.id"), primary_key=True)
)

account_record = Table(
    "account_record",
    Base.metadata,
    Column('record', BIGINT, ForeignKey("record.id"), primary_key=True),
    Column('account', BIGINT, ForeignKey("account.id"), primary_key=True),
    Column('operation', BIGINT, ForeignKey("operation_type.id"), primary_key=True),
    Column('amount', BIGINT, nullable=False)
)


class Record(Base, Mix):
    anotation = Column(VARCHAR(100), nullable=True)
    date = Column(DATE, nullable=False)
    amount = Column(BIGINT, nullable=False)
    my_tags = relationship('Tag', secondary=tag_recorde, back_populates='my_records')
    my_accounts = relationship('Account', secondary=account_record, back_populates='my_records')

    def __str__(self):
        return f'{self.anotation} at {str(self.date)} by {str(self.amount / 100)}'


class RecordData(DataModelDefault):
    anotation: Optional[str]
    date: Optional[date]
    amount: Optional[int]
    my_tags: Optional[list[int]]
    accounts: Optional[list[dict]]


class Service(ServiceDefault):

    def save(self, db: Session, data: RecordData) -> tuple[RecordData, int]:
        def fail(item_id: int) -> tuple[dict, int]:
            self.delete(db, item_id)
            return {"code": "Erro",
                    "text": "Informe account with account, operation and amount to Recorde"
                    }, status.HTTP_400_BAD_REQUEST

        _my_tags: list[int] = data.my_tags if "my_tags" in data.__dict__ else None
        _accounts: list[dict] = data.accounts if "accounts" in data.__dict__ else None
        _item, _status = super().save(db, data)
        if _status == status.HTTP_201_CREATED and "id" in _item:
            if _my_tags:
                for tag in _my_tags:
                    self.repository.raw_insert(db, tag_recorde, tag=tag, record=_item["id"])
            if _accounts: #TODO: check ammout sum
                for account_data in _accounts:
                    if ("account" in account_data and "amount" in account_data and
                            ("operation" in account_data or "operation_type" in account_data)):
                        self.repository.raw_insert(db, account_record, account=account_data["account"],
                                                   operation=account_data["operation"] \
                                                       if "operation" in account_data \
                                                       else account_data["operation_type"],
                                                   amount=account_data["amount"],
                                                   record=_item["id"])
                    else:
                        _item, _status = fail(_item["id"])
                        break
            else:
                _item, _status = fail(_item["id"])
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
