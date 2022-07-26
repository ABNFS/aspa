from pydantic import BaseModel
from typing import Optional

from .database import OperationType


class OperationTypeData(BaseModel):
    id: Optional[int]
    name: str
    alias: str
    deleted: Optional[bool]

    class Config:
        orm_mode = True

    def to_database(self, _db: Optional[OperationType] = None) -> OperationType:
        if self.id:
            if not _db:
                raise Exception("To update a object first find this object")
            _db.name = self.name if self.name else _db.name
            _db.alias = self.alias if self.alias else _db.alias
            _db.deleted = self.deleted if self.deleted else _db.deleted
            return _db
        return OperationType(name=self.name, alias=self.alias, deleted=self.deleted)
