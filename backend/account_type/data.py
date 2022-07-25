from typing import Optional
from pydantic import BaseModel

from .database import AccountType


class AccountTypeData(BaseModel):
    id: Optional[int]
    name: str
    alias: str
    operation: int
    deleted: Optional[bool]

    def to_database(self) -> AccountType:
        if self.id:
            return AccountType(id=self.id, name=self.name, alias=self.alias, deleted=self.deleted,
                               operation=self.operation if isinstance(self.operation, int) else self.operation.id)
        return AccountType(name=self.name, alias=self.alias, deleted=self.deleted,
                           operation=self.operation if isinstance(self.operation, int) else self.operation.id)
