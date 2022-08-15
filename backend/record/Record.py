from typing import Optional, ClassVar
from datetime import date

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import relationship, Session
from sqlalchemy import BIGINT, VARCHAR, DATE, Column, ForeignKey, Table, BOOLEAN

from default import ServiceDefault, ControllerDefault, DataModelDefault, Mix, MessageDataDefault, Base
from default.Default import ServiceError, log, RepositoryError, DefaultError
from account.Account import AccountService

tag_recorde = Table(
    "tag_record",
    Base.metadata,
    Column("record", ForeignKey("record.id"), primary_key=True),
    Column("tag", ForeignKey("tag.id"), primary_key=True)
)


class AccountRecord(Base):
    # thanks for https://stackoverflow.com/a/62378982/2638687
    __tablename__ = "account_record"

    record = Column(BIGINT, ForeignKey("record.id"), primary_key=True)
    account = Column(BIGINT, ForeignKey("account.id"), primary_key=True)
    operation = Column(BIGINT, ForeignKey("operation_type.id"), primary_key=True)
    value = Column(BIGINT, nullable=False)
    deleted = Column(BOOLEAN, default=False)

    this_record = relationship("Record", back_populates="accounts_record")
    account_in_record = relationship('Account', back_populates="my_records")
    account_in_record_operation_type = relationship('OperationType', back_populates="my_records")

    @property
    def id(self):
        return self.record

    def __str__(self):
        return f'{self.record}, {self.account}, {self.operation}'


class Record(Base, Mix):
    note = Column(VARCHAR(100), nullable=True)
    date = Column(DATE, nullable=False)
    total_amount = Column(BIGINT, nullable=False)
    my_tags = relationship('Tag', secondary=tag_recorde, back_populates='my_records')
    accounts_record = relationship('AccountRecord', back_populates='this_record')


class RecordAccountData(DataModelDefault):
    record: Optional[int]
    account: int
    operation: int
    value: int


class RecordData(DataModelDefault):
    note: Optional[str]
    date: Optional[date]
    total_amount: Optional[int]
    my_tags: Optional[list[int]]
    accounts: Optional[list[RecordAccountData]]


class AccountRecordService(ServiceDefault):
    def __init__(self):
        super().__init__(database_class=AccountRecord)


class RecordService(ServiceDefault):
    account_service: AccountService
    account_record_service: AccountRecordService

    def __init__(self):
        super().__init__(Record)
        self.account_service = AccountService()
        self.account_record_service = AccountRecordService()

    async def __fail__(self, db: Session,
                 item_id: int, msg: str = "Informe account with account, operation and amount to Recorde") \
            -> dict:
        async def delete_tags(id: int = None):
            await self.repository.raw_delete(db, table=tag_recorde, record=id)

        async def delete_account_records(id: int = None):
            account_repository = self.account_record_service.repository
            account_records: list[AccountRecord] = await account_repository.search_by_fields(db, AccountRecord, {"record": id})
            for account_rec in account_records:
                await account_repository.delete(db, AccountRecord, {
                    "record": account_rec.record,
                    "account": account_rec.account,
                    "operation": account_rec.operation})

        if item_id >= 0:
            try:
                await delete_tags(item_id)
                await delete_account_records(item_id)
                await self.delete(db, item_id)
            except DefaultError as e:
                log.debug(f'Error in delete itens saved with {e.message}')
                raise ServiceError(e.message)

        return {"code": "Erro",
                "text": msg
                }

    async def __new_record__(self, db: Session, item: dict, my_tags: Optional[list[int]] = None,
                       accounts: list[RecordAccountData] = None) -> dict:
        if my_tags:
            for tag in my_tags:
                try:
                    await self.repository.raw_insert(db, tag_recorde, tag=tag, record=item["id"])
                except RepositoryError as e:
                    log.debug(f'Error save tags into record: {e.message}')

        if accounts:
            # Every Record is doble-entry with 0 result (debit-credit=0)
            # Here record are composite with one or more accounts in operaton_type (D, C)
            #  each operation type sholde have value equal the operation per si.
            _sum: dict[int, int] = dict()

            for account_data in accounts:
                if not await self.account_service.can_operate(db=db, id=account_data.account):
                    return await self.__fail__(db, item["id"], f"Account {account_data.account} cannot operate.")

                account_data.record = item["id"]
                if account_data.operation in _sum:
                    _sum[account_data.operation] += account_data.value
                else:
                    _sum[account_data.operation] = account_data.value
                try:
                    await self.account_record_service.save(db=db, data=account_data)
                except ServiceError as e:
                    log.debug(f'Erro saving AccountRecord {e.message}')
                    raise ServiceError(e.message)

            for _s in _sum.values():
                if _s != item["total_amount"]:
                    return await self.__fail__(db, item["id"] if "id" in item else -1,
                                         "Total amount should be equals sum accounts by operation amount")
            return item
        else:
            return await self.__fail__(db, item["id"] if "id" in item else -1)

    async def save(self, db: Session, data: RecordData) -> dict:

        _my_tags: list[int] = data.my_tags if "my_tags" in data.__dict__ else None
        _accounts: list[RecordAccountData] = data.accounts if "accounts" in data.__dict__ else None
        try:
            saved = await super().save(db, data)
        except ServiceError as e:
            log.debug(f'Record Save Error: {e.message}')
            raise ServiceError(e.message)

        return await self.__new_record__(db, saved, _my_tags, _accounts)

class RecordController(ControllerDefault):
    def __init__(self):
        super().__init__(RecordService())

app = FastAPI()


@app.get("/{id}", response_class=JSONResponse, response_model=RecordData)
@app.get("/", response_class=JSONResponse, response_model=list[RecordData])
async def search(name: Optional[str] = '', id: Optional[int] = -1):
    return await RecordController().search(name=name, id=id)


@app.put("/", response_class=JSONResponse, response_model=list[RecordData])
@app.post("/", response_class=JSONResponse, response_model=list[RecordData], status_code=201)
async def create(record: RecordData | list[RecordData]):
    return await RecordController().new(data=record)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return await RecordController().delete(id=id, message_sucess={"code": "Ok", "text": f"Record {id} was deleted."})
