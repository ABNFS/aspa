from typing import Optional, ClassVar
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

    account_service: ServiceDefault

    def __init__(self, database_class: ClassVar = Record):
        from account.Account import Service as AccountService
        super().__init__(database_class)
        self.account_service = AccountService()

    def __fail__(self, db: Session,
                 item_id: int, msg: str = "Informe account with account, operation and amount to Recorde" ) \
            -> tuple[dict, int]:
        db.rollback()
        self.delete(db, item_id)
        return {"code": "Erro",
                "text": msg
                }, status.HTTP_400_BAD_REQUEST

    def __new_record__(self, db: Session, item: Record, my_tags: Optional[list[int]] = None, accounts: list[dict] = None):
        if my_tags:
            for tag in my_tags:
                self.repository.raw_insert(db, tag_recorde, commit=False, tag=tag, record=item["id"])

        if accounts:
            # Every Record is doble-entry with 0 result (debit-credit=0)
            # Here record are composite with one or more accounts in operaton_type (D, C)
            #  each operation type sholde have value equal the operation per si.
            _sum: dict[int, int] = dict()

            for account_data in accounts:
                if ("account" in account_data and "amount" in account_data and
                        ("operation" in account_data or "operation_type" in account_data)):

                    if not self.account_service.can_operate(db=db, id=account_data["account"]):
                        return self.__fail__(db, item["id"], f"Account {account_data['account']} cannot operate.")

                    if "operation_type" in account_data:
                        account_data["operation"] = account_data["operation_type"]

                    if account_data["operation"] in _sum:
                        _sum[account_data["operation"]] += account_data["amount"]
                    else:
                        _sum[account_data["operation"]] = account_data["amount"]

                    self.repository.raw_insert(db, account_record, commit=False,
                                               account=account_data["account"],
                                               operation=account_data["operation"],
                                               amount=account_data["amount"],
                                               record=item["id"])
                else:
                    return self.__fail__(item["id"])

            for _s in _sum.values():
                if _s != item["amount"]:
                    return self.__fail__(db, item["id"],
                                         "Total amount should be equals sum accounts by operation amount")
            db.commit()
            return item, status.HTTP_201_CREATED
        else:
            return self.__fail__(db, item["id"])

    def save(self, db: Session, data: RecordData) -> tuple[RecordData, int]:

        _my_tags: list[int] = data.my_tags if "my_tags" in data.__dict__ else None
        _accounts: list[dict] = data.accounts if "accounts" in data.__dict__ else None
        _item, _status = super().save(db, data)

        if _status == status.HTTP_201_CREATED and "id" in _item:
            _item, _status = self.__new_record__(db, _item, _my_tags, _accounts)
        return _item, _status


app = FastAPI()


@app.get("/{id}", response_class=JSONResponse, response_model=RecordData)
@app.get("/", response_class=JSONResponse, response_model=list[RecordData])
async def search(name: Optional[str] = '', id: Optional[int] = -1):
    return Controller(Service()).search(name=name, id=id)


@app.put("/", response_class=JSONResponse, response_model=list[RecordData])
@app.post("/", response_class=JSONResponse, response_model=list[RecordData], status_code=201)
async def create(record: RecordData | list[RecordData]):
    return Controller(Service()).new(data=record)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return Controller(Service()).delete(id=id, message_sucess={"code": "Ok", "text": f"Record {id} was deleted."})
