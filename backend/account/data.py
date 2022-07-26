from pydantic import BaseModel
from typing import Optional

from .database import Account


class AccountData(BaseModel):
    id: Optional[int]
    code: str
    name: str
    balance: Optional[int]
    alias: Optional[str]
    currency: Optional[int]
    account_type: int
    parent: Optional[int]
    operate: Optional[bool]
    deleted: Optional[bool]

    class Config:
        orm_mode = True

    def to_database(self, _db: Optional[Account] = None) -> Account:
        if self.id:
            if _db is None:
                Exception("For update Account first find the account to update")
            _db.code = self.code if self.code else _db.code
            _db.name = self.name if self.name else _db.name
            _db.alias = self.alias if self.alias else _db.alias
            _db.balance = self.balance if self.balance else _db.balance
            _db.currency = self.currency if self.currency else _db.currency
            _db.account_type = self.account_type if self.account_type else _db.account_type
            _db.parent = self.parent if self.parent else _db.parent
            _db.operate = self.operate if self.operate else _db.operate
            _db.deleted = self.deleted if self.deleted else _db.deleted
            return _db
        return Account(code=self.code, name=self.name, balance=self.balance, alias=self.alias,
                       currency=self.currency, account_type=self.account_type, parent=self.parent,
                       operate=self.operate, deleted=self.deleted)
