from typing import Optional

from pydantic import BaseModel

from .database import Currency


class CurrencyData(BaseModel):
    id: Optional[int]
    name: str
    alias: str
    default: Optional[bool]
    deleted: Optional[bool]

    class Config:
        orm_mode = True

    def to_database(self) -> Currency:
        if self.id:
            return Currency(id=self.id, name=self.name, alias=self.alias, default=self.default, deleted=self.deleted)
        return Currency(name=self.name, alias=self.alias, default=self.default, deleted=self.deleted)
