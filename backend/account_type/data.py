from typing import Optional
from pydantic import BaseModel

from .database import AccountType


class AccountTypeData(BaseModel):
    id: Optional[int]
    name: str
    alias: str
    operation: int
    deleted: Optional[bool]

    def to_database(self, _db: Optional[AccountType] = None) -> AccountType:
        if self.id:
            if not _db:
                raise Exception("Don't use this for existente AccountType, use get!!!")
            else:
                _db.name = self.name if self.name else _db.name
                _db.alias = self.alias if self.alias else _db.alias
                _db.deleted = self.deleted if self.deleted else _db.deleted
                _db.operation = self.operation if self.operation else _db.operation
                return _db
        return AccountType(name=self.name, alias=self.alias, deleted=self.deleted,
                           operation=self.operation if isinstance(self.operation, int) else self.operation.id)
