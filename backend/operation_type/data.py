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

    def to_database(self) -> OperationType:
        if self.id:
            return OperationType(id=self.id, name=self.name, alias=self.alias, deleted=self.deleted)
        return OperationType(name=self.name, alias=self.alias, deleted=self.deleted)