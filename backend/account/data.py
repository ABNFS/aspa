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

    def to_database(self) -> Account:
        if self.id:
            return Account(id=self.id, code=self.code, name=self.name, balance=self.balance, alias=self.alias,
                           currency=self.currency, account_type=self.account_type, parent=self.parent,
                           operate=self.operate, deleted=self.deleted)
        return Account(code=self.code, name=self.name, balance=self.balance, alias=self.alias,
                       currency=self.currency, account_type=self.account_type, parent=self.parent,
                       operate=self.operate, deleted=self.deleted)
